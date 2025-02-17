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

def log_in_user(passcode):
    move_on, message = validate_user(passcode)
    st.session_state.menu = move_on
    if move_on:
        record_question(question_passcode,passcode,passcode)
        set_username(passcode)
    st.sidebar.write(message)

passcode = st.sidebar.text_input(question_passcode, key="passcode")
log_in_button = st.sidebar.button('Log in', on_click=log_in_user, args=[passcode])

"""
# Wellcome to Stress Test!
Please answer the following questions and we'll create your account
"""

question_username = "What's your username?"
question_age = "Age"
question_focus_area = "Where would you like to focus?"
question_time_available = "How much time are you willing to spend in reducing stress?"
question_suggestions = "How many suggestions do you want?"
min_limit = 1
max_limit = 10

def create_user(user_username,user_passcode,age,focus_area,time_available,suggestions):
    move_on, message = new_user(user_username,user_passcode,age,focus_area,time_available,suggestions)
    st.session_state.menu = move_on
    if move_on:
        record_question(question_username,user_username,passcode)
        record_question(question_passcode,user_passcode,passcode)
        record_question(question_age,age,passcode)
        record_question(question_focus_area,focus_area,passcode)
        record_question(question_time_available,time_available,passcode)
        record_question(question_suggestions,suggestions,passcode)
        set_username(user_passcode)
    st.sidebar.write(message)

fake = Faker()
user_username = st.text_input(question_username, key="user_username", value=fake.user_name())
user_passcode = st.text_input(question_passcode, key="user_password", value=generate_unique_passcode(), disabled=True)
age = st.radio(question_age,("18-25", "26-35", "36-55", "56-70", "70+"))
focus_area = st.radio(question_focus_area,("Work/Career", "Finances", "Health & Well-being", "Relationships", "Time Management", "Personal Identity", "Major Life Changes", "Social Media & Technology", "Uncertainty & Future Planning"))
time_available = st.number_input(question_time_available, min_value=min_limit+2, max_value=2*max_limit)
suggestions = st.number_input(question_suggestions, min_value=min_limit, max_value=max_limit)
sign_in_button = st.button('Let us get started', on_click=create_user, args=[user_username,user_passcode,age, focus_area, time_available, suggestions])

def set_username (passcode):
    st.session_state.current_passcode = passcode

condition, index = get_status(st.session_state.current_passcode)

if st.session_state.menu and (sign_in_button or log_in_button) and index == -1 :
    st.switch_page("pages/status_page.py")
elif st.session_state.menu and (sign_in_button or log_in_button):
    st.switch_page("pages/main.py")
