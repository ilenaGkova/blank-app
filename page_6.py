import streamlit as st  # Streamlit Software
from mongo_connection import Tag, User, Favorite_Recommendation, Removed_Recommendation, Status, \
    Recommendation_Per_Person  # Database Function
from initialise_variables import initialize_variables  # Application Function
from user_information import add_points, change_recommendation_preference_for_user  # Database Function
from change_page import change_page  # Application Function

if 'page' not in st.session_state:
    st.session_state.page = 1  # Will set the layout the application will open

if 'current_passcode' not in st.session_state:
    st.session_state.current_passcode = 1  # Will register the user operating the application

if 'error' not in st.session_state:
    st.session_state.error = ''  # Will store error logs for functions called

if 'error_status' not in st.session_state:
    st.session_state.error_status = None  # Will indicate whether there is an error to show

if 'open_recommendation' not in st.session_state:
    st.session_state.open_recommendation = -1  # Will select a recommendation to open in full


def completed_recommendation(index_for_completed_recommendation,
                             status):  # Called when the user completes a recommendation

    st.session_state.error_status, st.session_state.error = add_points(index_for_completed_recommendation,
                                                                       st.session_state.current_passcode,
                                                                       status)  # Will update the session error variables and maybe increase the user's score if appropriate

    if st.session_state.error_status:  # Warning: The status variable is in reverse

        change_page(3)  # Will change the page to itself to reload and see the result


def change_recommendation_status(preference, index_for_change_recommendation_status,
                                 function=None):  # Will be called if the user wants to add / remove a recommendation form the favorite / removed category

    # Will update the session error variables and remove a recommendation from the favorite / removed category
    # Depending on whether the function parameter is None it will also add the recommendation either into the favorite or removed collection
    st.session_state.error_status, st.session_state.error = change_recommendation_preference_for_user(preference,
                                                                                                      st.session_state.current_passcode,
                                                                                                      index_for_change_recommendation_status,
                                                                                                      function)
    if st.session_state.error_status:  # Warning: The status variable is in reverse

        change_page(st.session_state.page)  # Will change the page to itself to reload and see the result


def layout_6():
    user, today, yesterday, index, recommendation = initialize_variables(st.session_state.current_passcode,
                                                                         st.session_state.open_recommendation)

    if recommendation is not None and user is not None and index != -1:

        # The Title

        with st.container(border=True):

            st.markdown(
                f"<div style='text-align: center;font-size: 40px;font-weight: bold;'>{recommendation['Title']}</div>",
                unsafe_allow_html=True)

        st.write("")  # Add a blank line for space
        st.write("")  # Add a blank line for space
        st.write("")  # Add a blank line for space
        st.write("")  # Add a blank line for space

        # Section 2: The Recommendation

        # Here we will show the description of the recommendation and the tags related
        # Tags are restrictive attributes that limit what kind of users will see this recommendation
        # Tags can be placed on time_available, stress_level, focus_area and age of a user
        # Too many tags means the recommendation may never be appropriate

        column_for_description_of_recommendation, column_for_tags_of_recommendation = st.columns(
            [5, 2])  # Seperate the line into 2 columns and name them after the content they hold

        with column_for_description_of_recommendation:

            with st.container(border=True):  # Add a square around the information

                st.write(recommendation['Description'])

                if recommendation['Link'] is not None:
                    st.write('See more information on ', recommendation['Link'])  # Show a link if one exists

                # Each column is named after the content it shows

                column_for_outcome, column_for_reference_1, column_for_reference_2 = st.columns([7, 0.5, 0.5])

                # Preference indicates if the recommendation is in the favorite/removed or no section for this user.
                # Depending on that the user will see a different combination of buttons
                # A recommendation can't be both in the favorite and removed section. To be in one it will be removed from the other.

                with column_for_outcome:

                    if Recommendation_Per_Person.find_one(
                            {"ID": recommendation['ID'], "Passcode": st.session_state.current_passcode,
                             "Status_Created_At": Status.find_one({"_id": index})[
                                 'Created_At'], "Outcome": True}):  # Mirrors how the recommendation_per_person stores recommendation outcomes

                        st.button("", icon=":material/done_outline:", use_container_width=True,
                                  on_click=completed_recommendation,
                                  args=[recommendation['ID'], Status.find_one({"_id": index})['Created_At']],
                                  key=f"complete_open_user_recommendation_generated_list_with_recommendations_{recommendation['ID']}")

                with column_for_reference_1:

                    if Removed_Recommendation.find_one(
                            {"ID": recommendation['ID'], "Passcode": st.session_state.current_passcode}):
                        st.button("", icon=":material/thumb_up:", use_container_width=True,
                                  on_click=change_recommendation_status, args=[1, recommendation['ID'], False],
                                  key=f"love_open_user_recommendation_generated_list_with_recommendations_{recommendation['ID']}")

                    elif Favorite_Recommendation.find_one(
                            {"ID": recommendation['ID'], "Passcode": st.session_state.current_passcode}):
                        st.button("", icon=":material/delete:", use_container_width=True,
                                  on_click=change_recommendation_status,
                                  args=[1, recommendation['ID'], True],
                                  key=f"remove_recommendation_open_user_recommendation_generated_list_with_recommendations_{recommendation['ID']}_x")

                    else:
                        st.button("", icon=":material/thumb_up:", use_container_width=True,
                                  on_click=change_recommendation_status, args=[1, recommendation['ID'], False],
                                  key=f"love_open_user_recommendation_generated_list_with_recommendations_{recommendation['ID']}_y")

                with column_for_reference_2:

                    if Removed_Recommendation.find_one(
                            {"ID": recommendation['ID'], "Passcode": st.session_state.current_passcode}):
                        st.button("", icon=":material/delete:", use_container_width=True,
                                  on_click=change_recommendation_status,
                                  args=[-1, recommendation['ID'], True],
                                  key=f"remove_recommendation_open_user_recommendation_generated_list_with_recommendations_{recommendation['ID']}")

                    elif Favorite_Recommendation.find_one(
                            {"ID": recommendation['ID'], "Passcode": st.session_state.current_passcode}):
                        st.button("", icon=":material/thumb_down:", use_container_width=True,
                                  on_click=change_recommendation_status, args=[-1, recommendation['ID'], False],
                                  key=f"hate_open_user_recommendation_generated_list_with_recommendations_{recommendation['ID']}_x")

                    else:
                        st.button("", icon=":material/thumb_down:", use_container_width=True,
                                  on_click=change_recommendation_status, args=[-1, recommendation['ID'], False],
                                  key=f"hate_open_user_recommendation_generated_list_with_recommendations_{recommendation['ID']}_y")

        with column_for_tags_of_recommendation:

            # Here we will show all tags related since they exist now
            # We will include the category they are in and their value and well as the username of the person who added them

            st.write("Tags related to this recommendation:")

            tags = list(Tag.find({"ID": recommendation['ID']}))  # Get list of tags related

            for entry_in_tags in tags:
                # Warning: The creator is stored by passcode, but the passcode is how users sign in the application
                # Showing it here would give everyone the ability to take on the admins identity

                st.write(entry_in_tags['Title_Of_Criteria'], ': ', entry_in_tags['Category'], 'as assigned by, ',
                         User.find_one({"Passcode": entry_in_tags['Passcode']})[
                             'Username'])  # To avoid data leakage we will show the creator by username

    elif user is not None and index != -1:

        st.session_state.error_status = False
        st.session_state.error = f"Something went wrong, Recommendation with ID number {st.session_state.open_recommendation} not found."
