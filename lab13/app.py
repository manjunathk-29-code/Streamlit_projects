
import streamlit as st
import pandas as pd


from db import (
    init_db,
    create_user,
    get_user_by_username,
    get_all_users,
    user_exists
)

from auth import (
    hash_password,
    verify_password,
    validate_username,
    validate_email,
    validate_password
)



# -----------------------------------
# 1. Page configuration
# -----------------------------------
st.set_page_config(
    page_title="Auth App",
    page_icon="🔐",
    layout="centered"
)


# -----------------------------------
# 2. Initialize database
# -----------------------------------
@st.cache_resource
def setup_database():
    init_db()
    return True


try:
    setup_database()
except Exception as e:
    st.error("Registration failed.")
    st.code(str(e))


# -----------------------------------
# 3. Initialize session state
# -----------------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = None

# Exercise 3: Count failed login attempts
if "attempts" not in st.session_state:
    st.session_state.attempts = 0


# -----------------------------------
# 4. Sign-up page
# -----------------------------------
def signup_page():
    st.title("Create Account")

    with st.form("signup_form"):
        username = st.text_input("Username")
        email = st.text_input("Email")
        password = st.text_input(
            "Password",
            type="password"
        )
        confirm = st.text_input(
            "Confirm Password",
            type="password"
        )

        submit = st.form_submit_button(
            "Sign Up",
            use_container_width=True
        )

    if submit:
        username = username.strip()
        email = email.strip()

        # Validate username
        ok, msg = validate_username(username)
        if not ok:
            st.error(msg)
            return

        # Validate email
        ok, msg = validate_email(email)
        if not ok:
            st.error(msg)
            return

        # Validate password
        ok, msg = validate_password(password)
        if not ok:
            st.error(msg)
            return

        # Confirm password
        if password != confirm:
            st.error("Passwords do not match.")
            return

        # Check existing username and email
        if user_exists(username=username):
            st.error("Username already taken.")
            return

        if user_exists(email=email):
            st.error("Email already registered.")
            return

        # Create account with hashed password
        try:
            success = create_user(
                username,
                email,
                hash_password(password)
            )

            if success:
                st.success(
                    "Account created successfully! "
                    "Please log in."
                )
            else:
                st.error("Could not create your account.")

        except Exception as e:
            st.error("Registration failed.")
            st.code(str(e))


# -----------------------------------
# 5. Login page
# -----------------------------------
def login_page():
    st.title("Welcome Back")

    # Exercise 3: Show lockout status
    if st.session_state.attempts >= 3:
        st.error(
            "Too many failed attempts. "
            "Login is locked for this session."
        )
        return

    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input(
            "Password",
            type="password"
        )

        submit = st.form_submit_button(
            "Login",
            use_container_width=True
        )

    if submit:
        username = username.strip()

        try:
            user = get_user_by_username(username)

            # Check username and password
            if (
                user is not None
                and verify_password(
                    password,
                    user["password_hash"]
                )
            ):
                # Successful login: reset attempts
                st.session_state.attempts = 0
                st.session_state.logged_in = True

                # Exercise 2: Store the user's role
                st.session_state.user = {
                    "id": user["id"],
                    "username": user["username"],
                    "email": user["email"],
                    "created_at": user["created_at"],
                    "role": user["role"]
                }

                st.rerun()

            else:
                # Exercise 3: Count failed login
                # attempts
                st.session_state.attempts += 1

                if st.session_state.attempts >= 3:
                    st.error(
                        "Too many failed attempts. "
                        "Login is locked for this session."
                    )
                else:
                    remaining = (
                        3 - st.session_state.attempts
                    )

                    st.error(
                        "Invalid username or password. "
                        f"Attempt {st.session_state.attempts}/3. "
                        f"{remaining} attempt(s) remaining."
                    )

        except Exception as e:
            st.error("Login failed.")
            st.code(str(e))


# -----------------------------------
# 6. Dashboard page
# -----------------------------------
def dashboard_page():
    user = st.session_state.user

    st.title(f"Welcome, {user['username']}! 👋")
    st.write("You are successfully logged in.")

    col1, col2 = st.columns(2)

    col1.metric("User ID", user["id"])
    col2.metric("Username", user["username"])

    st.write("**Email:**", user["email"])
    st.write("**Role:**", user["role"].title())

    if user["created_at"]:
        st.write(
            "**Joined:**",
            user["created_at"].strftime(
                "%Y-%m-%d %H:%M"
            )
        )

    st.divider()

    # -----------------------------------
    # Exercise 2: Admin-only access
    # -----------------------------------
    if user["role"] == "admin":
        st.subheader("🛡️ Admin Panel")
        st.write(
            "You have administrator access. "
            "You can view all registered users."
        )

        try:
            users = get_all_users()

            if users:
                df = pd.DataFrame(users)

                if "created_at" in df.columns:
                    df["created_at"] = pd.to_datetime(
                        df["created_at"]
                    ).dt.strftime("%Y-%m-%d %H:%M")

                st.dataframe(
                    df,
                    use_container_width=True,
                    hide_index=True
                )
            else:
                st.info("No registered users found.")

        except Exception as e:
            st.error("Could not load registered users.")
            st.code(str(e))

    else:
        st.info(
            "You have normal user access. "
            "The Admin Panel is available only to admins."
        )

    st.divider()

    # Logout
    if st.button("Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.user = None

        # Reset attempts when logging out
        st.session_state.attempts = 0

        st.rerun()


# -----------------------------------
# 7. Main application navigation
# -----------------------------------
if st.session_state.logged_in:
    dashboard_page()

else:
    st.title("User Authentication System")

    tab_login, tab_signup = st.tabs(
        ["Login", "Sign Up"]
    )

    with tab_login:
        login_page()

    with tab_signup:
        signup_page()
