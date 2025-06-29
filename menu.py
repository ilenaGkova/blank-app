import streamlit as st  # Streamlit Software
from initialise_variables import initialize_variables  # Application Function
from change_page import change_page  # Application Function

if 'current_passcode' not in st.session_state:
    st.session_state.current_passcode = 1  # Will register the user operating the application

if 'open_recommendation' not in st.session_state:
    st.session_state.open_recommendation = -1  # Will select a recommendation to open in full

if 'error' not in st.session_state:
    st.session_state.error = ''  # Will store error logs for functions called

if 'error_status' not in st.session_state:
    st.session_state.error_status = None  # Will indicate whether there is an error to show


def menu_layout():
    user, today, yesterday, index, recommendation = initialize_variables(st.session_state.current_passcode,
                                                                         st.session_state.open_recommendation)

    # After the point the user sees the same menu in each of the next pages

    # Layouts and numbers assigned
    # 1 is the page where the user makes a new account or signs in with their passcode
    # 2 is the page where the user can answer questions about stress levels
    # 3 is the home page where the user can see and complete recommendations
    # 4 is the profile and preferences page where the user can update their profile and manage their preferences
    # 5 is the Record page where the user can see their application history
    # 6 is the page where the user can see a recommendation in full
    # 7 is the tutorial page where the user can see how the application works
    # 8 is the page where the user can make a confession and manage their confessions
    # 9 is the page where an admin can add entries to the collections of the database

    st.sidebar.markdown(f"<div style='text-align: center;font-size: 20px; font-weight: bold;'>Navigation Menu</div>",
                        unsafe_allow_html=True)

    st.sidebar.write("")  # Add blank line

    if user is not None and index != -1:  # Users have a more limited menu than an admin

        if user['Role'] != 'User':
            st.sidebar.button('Add Data to Stress Test Database', icon=":material/add_circle:",
                              use_container_width=True,
                              on_click=change_page,
                              args=[9], key="admin_add_page_admin")

        st.sidebar.button("Home", icon=":material/home:", use_container_width=True, on_click=change_page, args=[3],
                          key="main_page")
        st.sidebar.button("Profile and Preferences", icon=":material/person_3:", use_container_width=True,
                          on_click=change_page, args=[4], key="profile_page")
        st.sidebar.button("Daily Stress Questionnaire", icon=":material/add:", use_container_width=True,
                          on_click=change_page,
                          args=[2], key="status_page")
        st.sidebar.button("See Record", icon=":material/clinical_notes:", use_container_width=True,
                          on_click=change_page, args=[5], key="record_page")
        st.sidebar.button('Make a confession', icon=":material/draw:", use_container_width=True,
                          on_click=change_page,
                          args=[8], key="make_confession")
        st.sidebar.button("See Tutorial", icon=":material/auto_stories:", use_container_width=True,
                          on_click=change_page, args=[7], key="tutorial_page")
        st.sidebar.button("Exit", icon=":material/logout:", use_container_width=True, on_click=change_page, args=[1],
                          key="log_out")

    elif user is None:

        # Page won't open unless user is registered

        st.session_state.error_status = False
        st.session_state.error_status = "Something went wrong, user not registered."

    else:

        # Page won't open unless user has made a status  is registered

        st.session_state.error_status = False
        st.session_state.error_status = "Something went wrong, status not found."
