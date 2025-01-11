import streamlit as st
from mongo_connection import validate_user, new_user

st.set_page_config(
    page_title="Log In",
    page_icon="👋",
)

if "menu" not in st.session_state:
    st.session_state.menu = False

def set_username (username):
    if "current_username" not in st.session_state:
        st.session_state.current_username = username

def log_in_user(username, password):
    move_on, message = validate_user(username, password)
    st.session_state.menu = move_on
    st.sidebar.write(message)

def create_user(first_name,last_name,user_username,user_password,chosen):
    move_on, message = new_user(first_name,last_name,user_username,user_password,chosen)
    st.session_state.menu = move_on
    st.write(message)

st.sidebar.write ('Already have an account? Sign it!')
username = st.sidebar.text_input("Your Username", key="username")
password = st.sidebar.text_input("Your Password", key="password")
st.sidebar.button('Log in', on_click=log_in_user, args=[username, password])

"""
# Wellcome to Stress Test!
Please answer the following questions and we'll create your account
"""
first_name = st.text_input("What's your first name?", key="first_name")
last_name = st.text_input("What's your last name?", key="last_name")
user_username = st.text_input("What's your username?", key="user_username")
user_passname = st.text_input("What's your password?", key="user_password")
chosen = st.radio('Age',("18-25", "26-35", "36-55", "56-70", "70+"))
st.button('Let us get started', on_click=create_user, args=[first_name,last_name,username,password,chosen])


start_page = st.Page("streamlit_app.py", title="Sign Me In")
status_page = st.Page("pages/status_page.py", title="Make My Status")
if st.session_state.menu:
    pg =st.navigation([start_page, status_page])
else:
    pg =st.navigation([start_page, status_page], position="hidden")

