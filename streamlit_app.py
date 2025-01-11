import streamlit as st
from mongo_connection import validate_user, new_user

st.set_page_config(
    page_title="Log In",
    page_icon="👋",
)

def log_in_user(username, password):
    move_on, message = validate_user(username, password)
    st.sidebar.write(message)

def create_user(first_name,last_name,username,password,chosen):
    move_on, message = new_user(first_name,last_name,username,password,chosen)
    st.write(message)

st.sidebar.write ('Already have an account? Sign it!')
username = st.sidebar.text_input("Your Username", key="username")
password = st.sidebar.text_input("Your Password", key="password")
st.sidebar.button('Log in', on_click=log_in_user, args=[username, password])

"""
# Wellcome to Stress Test!
Please answer the following questions and we'll create your account
"""
st.text_input("What's your first name?", key="first_name")
st.text_input("What's your last name?", key="last_name")
st.text_input("What's your username?", key="user_username")
st.text_input("What's your password?", key="user_password")
chosen = st.radio(
        'Age',
        ("18-25", "26-35", "36-55", "56-70", "70+"))
st.button('Let us get started', on_click=create_user, args=[first_name,last_name,username,password,chosen])

