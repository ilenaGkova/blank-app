import streamlit as st  # Streamlit Software
from initialise_variables import initialize_variables, options, question_passcode  # Application Function
from check_and_balance import record_question, record_status  # Database Function
from change_page import change_page  # Application Function
from mongo_connection import Question_Questionnaire  # Database Function
# Application Function

if 'page' not in st.session_state:
    st.session_state.page = 1  # Will set the layout the application will open

if 'current_passcode' not in st.session_state:
    st.session_state.current_passcode = 1  # Will register the user operating the application

if 'error' not in st.session_state:
    st.session_state.error = ''  # Will store error logs for functions called

if 'error_status' not in st.session_state:
    st.session_state.error_status = None  # Will indicate whether there is an error to show


def submit_questionnaire(q1, q2, q3, q4, q5, a1, a2, a3, a4, a5):
    """
    Called when the user completes the questionnaire.
    Calculates total stress level from q1-q5 questions and answers and submits the averaged stress level.
    """

    # List of (question, answer) pairs directly from input
    question_answer_pairs = [(q1, a1), (q2, a2), (q3, a3), (q4, a4), (q5, a5)]

    stress_level = 0  # Initialize stress level to 0

    # Process each question-answer pair
    for question, answer in question_answer_pairs:
        # catalog_question records and returns the numeric stress value
        stress_level += catalog_question(question, answer, st.session_state.current_passcode)

    # Calculate average stress level
    average_stress = float(stress_level) / len(question_answer_pairs)

    # Submit the final stress level
    make_status(average_stress)


def catalog_question(question, answer, passcode):  # Called for each question in the Daily Stress Questionnaire

    record_question(question, answer, passcode)  # We need record the answer the user gave to a question everytime the user enters something in a field or selects an answer out of a radio button

    return options.get(answer)  # Depending on the answer the stress level will rise by 0 through 4


def make_status(
        user_stress_level):  # Called when the user makes a status by answering questions about their stress level

    st.session_state.error_status, st.session_state.error = record_status(st.session_state.current_passcode,
                                                                          user_stress_level)  # Will update the session error variables and maybe create new status for user if appropriate

    if st.session_state.error_status:  # Warning: The status variable is in reverse

        change_page(3)  # Will can function to move to Home page


def layout_2():

    user, today, yesterday, index, recommendation = initialize_variables(st.session_state.current_passcode,
                                                                         1)

    if user is not None:

        # The SideBar - User Information

        # Show the user information and preferences

        st.sidebar.write("Questions generated after studying the symptoms of stress")
        st.sidebar.write("Citation provided:")
        st.sidebar.write("C. Acred, Anxiety and stress. Cambridge: Independence Educational Publishers, 2015.")

        if today:  # Sometimes users do multable statuses a day, if one has been done the user doesn't need to make another unless they want to

            st.sidebar.button('Skip', on_click=change_page, args=[3], use_container_width=True, key="skip")

        # The Title

        st.title(f"Hello {user['Username']}")

        if int(user['Days_Summed']) <= 1:
            with st.container(border=True):
                st.header(f"See your passcode here:")
                st.text_input("", value=st.session_state.current_passcode, key="passcode", type="password")
                st.write(f"This message will only appear today. Please remember your passcode to log in next time!")

        st.header("""Please answer the Daily Stress Questioner""")

        # The Daily Question Section
        # For each question we will have a slider for the user to answer

        with st.container(border=True):
            a1 = st.select_slider(f"Today I felt that I couldn't cope with the important things I had to do", list(options.keys()), key="question_1")

        with st.container(border=True):
            a2 = st.select_slider(f"Today I felt anxious and worried without a specific reason", list(options.keys()), key="question_2")

        with st.container(border=True):
            a3 = st.select_slider(f"Today I had physical symptoms such as rapid heartbeat, chest or stomach pain, sweating", list(options.keys()), key="question_3")

        with st.container(border=True):
            a4 = st.select_slider(f"Today I had difficulty taking care of my daily needs (food, hygiene)", list(options.keys()), key="question_4")

        with st.container(border=True):
            a5 = st.select_slider(f"Today I felt anger, fear, or a lack of self-confidence", list(options.keys()), key="question_5")

        st.button("Submit", on_click=submit_questionnaire, args=[f"Today I felt that I couldn't cope with the important things I had to do", f"Today I felt anxious and worried without a specific reason", f"Today I had physical symptoms such as rapid heartbeat, chest or stomach pain, sweating", f"Today I had difficulty taking care of my daily needs (food, hygiene)", f"Today I felt anger, fear, or a lack of self-confidence", a1, a2, a3, a4, a5], use_container_width=True, key="make_status")  # Step 2: Click button to submit answers

    else:

        # Page won't open unless user is registered

        st.session_state.error_status = False
        st.session_state.error_status = "Something went wrong, user not registered."
