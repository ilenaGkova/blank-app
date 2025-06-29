import streamlit as st  # Streamlit Software
from initialise_variables import initialize_variables, con_question  # Application Function
from check_and_balance import record_question  # Database Function
from mongo_connection import Question  # Database Function
from make_record import delete_entry  # Database Function


if 'current_passcode' not in st.session_state:
    st.session_state.current_passcode = 1  # Will register the user operating the application

if 'error' not in st.session_state:
    st.session_state.error = ''  # Will store error logs for functions called

if 'error_status' not in st.session_state:
    st.session_state.error_status = None  # Will indicate whether there is an error to show


def layout_8():

    user, today, yesterday, index, recommendation = initialize_variables(st.session_state.current_passcode,
                                                                         1)

    if user is not None and index != -1:

        # The Title

        # We save title in a variable to record the confession as a question
        # To record a question we need a question, an answer and a passcode
        # We also search when by the question in the question collection to show the user their previous confessions
        # We don't show any other kind of questions in this page

        st.title(con_question)

        confession_form_layout()

        confession_list_layout()

    else:

        st.session_state.error_status = False

        if user is None and index == -1:
            st.session_state.error = 'Something went wrong, User not signed in and no Status found'
        elif user is None:
            st.session_state.error = 'Something went wrong, no Status found'
        else:
            st.session_state.error = 'Something went wrong, User not signed in'


def confession_list_layout():
    # Section 2: The Older Confessions
    # The Title
    st.header("Your previous confessions:")
    data = list(Question.find({"Passcode": st.session_state.current_passcode,
                               "Question": con_question}))  # Search for only this question in the question collection
    # Depending on the number of confessions, we show different messages before listing them
    if len(data) == 0:

        st.write("You haven't entered any confessions yet")

    elif len(data) == 1:

        st.write("You have made 1 confession")

    else:

        st.write(f"You have made {len(data)} confessions")
    pointer_for_confessions = 1  # Pointer works as unique identifier of the button and separates the confessions for the user
    for entry in data:
        with st.container(border=True):  # Box each entry to seperate them

            column_for_pointer_for_confession, column_for_timestamp_for_confession, column_for_confession, column_for_delete_confession_button = st.columns(
                [1, 2, 4, 0.5])  # Columns are named after the content they show

            with column_for_pointer_for_confession:
                st.write(pointer_for_confessions)  # Show pointer so seperate confessions

            with column_for_timestamp_for_confession:
                st.write(entry['Created_At'])  # When the confession was made

            with column_for_confession:
                st.write(entry['Answer'])  # Show the confession

            with column_for_delete_confession_button:
                # We use a generalised function that takes a collection name, some key information and deletes an entry from the collection
                # For the Question Collection we need the question, the user, and the time created to delete the entry

                st.button('', icon=":material/delete:", use_container_width=True,
                          on_click=delete_entry,
                          args=[st.session_state.current_passcode, entry['Question'], None, entry['Created_At'],
                                "Question", st.session_state.current_passcode],
                          key=f"delete_confession_button_{pointer_for_confessions}")

        pointer_for_confessions += 1


def confession_form_layout():
    # Section 1: The New Confession
    with st.container(border=True):  # Put a square around this to seperate from anything else

        answer = st.text_area("",
                              height=300)  # Warning: Alike other input text filed this type need control+enter to save the new information

        # This application is not very private.
        # We add a disclaimer to warn the user to keep their information private
        # Putting it in text makes it easy to ignore, so it's a checkbox instead

        disclaimer = st.checkbox(
            "I have not entered any identifying or sensitive information such as full names or banking information.")

        # Usually record question takes 3 variables: passcode, question and answer
        # Only this time we also sent the disclaimer as a forth
        # See the mongo file for more information

        st.button("Enter confession", icon=":material/draw:", use_container_width=True,
                  on_click=record_question,
                  args=[con_question, answer, st.session_state.current_passcode, disclaimer],
                  key="add_confession_button_in_page")
