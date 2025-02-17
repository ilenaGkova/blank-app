import streamlit as st

st.set_page_config(
    page_title="Log In",
    page_icon="👋",
)

from mongo_connection import generate_unique_passcode, get_status, validate_user, new_user, record_question
from faker import Faker

if "menu" not in st.session_state:
    st.session_state.menu = False

if "current_passcode" not in st.session_state:
    st.session_state.current_passcode = 1

st.sidebar.write ('Already have an account? Sign it!')

question_passcode = "What's your passcode?"

def log_in_user(password):
    move_on, message = validate_user(password)
    st.session_state.menu = move_on
    if move_on:
        record_question(question_passcode,password,password)
        set_username(password)
    st.sidebar.write(message)

passcode = st.sidebar.text_input(question_passcode, key="passcode")
log_in_button = st.sidebar.button('Log in', on_click=log_in_user, args=[passcode])

"""
# Wellcome to Stress Test!
Please answer the following questions and we'll create your account
"""

question_username = "What's your username?"
question_age = "Age"

def create_user(user_username,user_passcode,age):
    move_on, message = new_user(user_username,user_passcode,age)
    st.session_state.menu = move_on
    if move_on:
        record_question(question_username,user_username,user_username)
        record_question(question_passcode,user_passcode,user_username)
        record_question(question_age,age,user_username)
        set_username(user_passcode)
    st.sidebar.write(message)

fake = Faker()
user_username = st.text_input(question_username, key="user_username", value=fake.user_name())
user_passcode = st.text_input(question_passcode, key="user_password", value=generate_unique_passcode(), disabled=True)
age = st.radio(question_age,("18-25", "26-35", "36-55", "56-70", "70+"))
sign_in_button = st.button('Let us get started', on_click=create_user, args=[user_username,user_passcode,age])

def set_username (passcode):
    st.session_state.current_passcode = passcode

condition, index = get_status(st.session_state.current_passcode)

if st.session_state.menu and (sign_in_button or log_in_button) and index == -1 :
    st.switch_page("pages/status_page.py")
elif st.session_state.menu and (sign_in_button or log_in_button):
    st.switch_page("pages/main.py")
