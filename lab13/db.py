
import streamlit as st
import psycopg2
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager


# 1. Connect to PostgreSQL
@contextmanager
def get_connection():
    conn = None

    try:
        # Option 1: Connect using a database URL
        if "url" in st.secrets["postgres"]:
            conn = psycopg2.connect(
                st.secrets["postgres"]["url"],
                cursor_factory=RealDictCursor
            )

        # Option 2: Connect using individual settings
        else:
            conn = psycopg2.connect(
                host=st.secrets["postgres"]["host"],
                port=st.secrets["postgres"]["port"],
                database=st.secrets["postgres"]["database"],
                user=st.secrets["postgres"]["user"],
                password=st.secrets["postgres"]["password"],
                cursor_factory=RealDictCursor
            )

        yield conn
        conn.commit()

    except Exception:
        if conn is not None:
            conn.rollback()
        raise

    finally:
        if conn is not None:
            conn.close()


# 2. Create the users table if it doesn't exist
def init_db():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    email VARCHAR(100) UNIQUE NOT NULL,
                    password_hash VARCHAR(255) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)


# 3. Register a new user
def create_user(username, email, password_hash):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO users
                        (username, email, password_hash)
                    VALUES (%s, %s, %s)
                    """,
                    (username, email, password_hash)
                )

        return True

    except psycopg2.errors.UniqueViolation:
        return False


# 4. Find a user by username
def get_user_by_username(username):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM users WHERE username = %s",
                (username,)
            )
            return cur.fetchone()


# 5. Get all registered users
def get_all_users():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, username, email, created_at
                FROM users
                ORDER BY id
            """)
            return cur.fetchall()


# 6. Check whether a username or email exists
def user_exists(username=None, email=None):
    if username is None and email is None:
        return False

    with get_connection() as conn:
        with conn.cursor() as cur:
            if username is not None:
                cur.execute(
                    "SELECT 1 FROM users WHERE username = %s",
                    (username,)
                )
            else:
                cur.execute(
                    "SELECT 1 FROM users WHERE email = %s",
                    (email,)
                )

            return cur.fetchone() is not None


# 7. Update a user's password hash
def update_password(username, new_hash):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE users
                SET password_hash = %s
                WHERE username = %s
                """,
                (new_hash, username)
            )

            return cur.rowcount > 0
