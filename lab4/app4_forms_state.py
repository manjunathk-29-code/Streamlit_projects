
import streamlit as st

st.title("Forms + Session State")

# --- Counter using session_state ---
if "count" not in st.session_state:
    st.session_state.count = 0

if st.button("Increment"):
    st.session_state.count += 1

st.write("Counter:", st.session_state.count)

# --- Login Form ---
with st.form("login_form"):
    st.subheader("Login")

    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")

    submit = st.form_submit_button("Login")

if submit:
    if user == "admin" and pwd == "1234":
        st.session_state.logged_in = True
        st.success("Login successful!")
    else:
        st.session_state.logged_in = False
        st.error("Invalid credentials")

if st.session_state.get("logged_in", False):
    st.info("Welcome, admin! You are now logged in.")

# --- Counter with Multiple Buttons ---
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Increment more"):
        st.session_state.count += 1

with col2:
    if st.button("Add 5"):
        st.session_state.count += 5

with col3:
    if st.button("Reset"):
        st.session_state.count = 0

st.write("Counter:", st.session_state.count)

# --- To-Do List using Session State ---
if "todos" not in st.session_state:
    st.session_state.todos = []

with st.form("todo_form", clear_on_submit=True):
    task = st.text_input("New Task")
    add = st.form_submit_button("Add Task")

if add and task.strip():
    st.session_state.todos.append(task.strip())

st.subheader("Your Tasks")

for i, t in enumerate(st.session_state.todos):
    st.write(f"{i + 1}. {t}")

if st.button("Clear All"):
    st.session_state.todos = []
    st.rerun()
