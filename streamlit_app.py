import streamlit as st
from mongo_connection import get_database

st.set_page_config(
    page_title="Log In",
    page_icon="👋",
)

def log_in_user(username, password):
    query = {
        'username': username,
        'password': password
    }
    data = get_database()
    if data is not None:
        user_collection = data['StressApp']['User']
        if user_collection.count_documents(query) == 0:
            st.sidebar.write('You do not have an account')
        else:
            st.sidebar.write('You have an account')
        return True
    else:
        st.error("Database connection not established. Please check your connection settings.")
        st.sidebar.write('No database connection - try again later')
        return False

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
st.button('Let us get started')

