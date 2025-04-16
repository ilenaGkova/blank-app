import streamlit as st  # Streamlit Software

if "page" not in st.session_state:
    st.session_state.page = 1  # Will set the layout the application will open

if 'error_status' not in st.session_state:
    st.session_state.error_status = None  # Will indicate whether there is an error to show


def change_page(new_page):  # This function will change the page

    st.session_state.page = new_page  # By changing the page number we change the layout
    st.session_state.error_status = True  # Will reset the status of the error message, so it doesn't follow the user


def open_recommendation(index_for_open_recommendation):  # Called when user wants to see a recommendation in full

    st.session_state.open_recommendation = index_for_open_recommendation  # Will set the recommendation to be opened

    change_page(6)  # Will change page layout to show the recommendation
