import streamlit as st
from mongo_connection import get_status, validate_user, new_user, record_question
from Tables import Questions

st.set_page_config(
    page_title="Log In",
    page_icon="👋",
)

if "menu" not in st.session_state:
    st.session_state.menu = False

if "current_username" not in st.session_state:
    st.session_state.current_username = "username"

st.sidebar.write ('Already have an account? Sign it!')

def log_in_user(username, password):
    move_on, message = validate_user(username, password)
    st.session_state.menu = move_on
    if move_on:
        set_username(username)
    st.sidebar.write(message)

username = st.sidebar.text_input("Your Username", key="username")
password = st.sidebar.text_input("Your Password", key="password")
log_in_button = st.sidebar.button('Log in', on_click=log_in_user, args=[username, password])

"""
# Wellcome to Stress Test!
Please answer the following questions and we'll create your account
"""

question_first_name = "What's your first name?"
question_last_name = "What's your last name?"
question_username = "What's your username?"
question_password = "What's your password?"
question_age = "Age"

def create_user(first_name,last_name,user_username,user_password,age):
    move_on, message = new_user(first_name,last_name,user_username,user_password,age)
    st.session_state.menu = move_on
    if move_on:
        record_question(question_first_name,first_name,user_username)
        record_question(question_last_name,last_name,user_username)
        record_question(question_username,user_username,user_username)
        record_question(question_password,user_password,user_username)
        record_question(question_age,age,user_username)
        set_username(user_username)
    st.write(message)

first_name = st.text_input(question_first_name, key="first_name")
last_name = st.text_input(question_last_name, key="last_name")
user_username = st.text_input(question_username, key="user_username")
user_password = st.text_input(question_password, key="user_password")
age = st.radio(question_age,("18-25", "26-35", "36-55", "56-70", "70+"))
sign_in_button = st.button('Let us get started', on_click=create_user, args=[first_name,last_name,user_username,user_password,age])

def set_username (username):
    st.session_state.current_username = username 

condition, index = get_status(st.session_state.current_username)

if st.session_state.menu and (sign_in_button or log_in_button) and index == -1 :
    st.switch_page("pages/status_page.py")
elif st.session_state.menu and (sign_in_button or log_in_button):
    st.switch_page("pages/main.py")
