import streamlit as st

# Configuration Command

st.set_page_config(
    page_title="StressTest",
    page_icon="👋",
)

# Additional Imports

from mongo_connection import insert_data

if 'page' not in st.session_state:
    st.session_state.page = 1  # Will set the layout the application will open

if 'error' not in st.session_state:
    st.session_state.error = ''  # Will store error logs for functions called

if 'error_status' not in st.session_state:
    st.session_state.error_status = None  # Will indicate whether there is an error to show

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
# 10 is the evaluation page where the admin can do the evaluation

# Step 1: Show the error if needed

if st.session_state.error_status is not None and not st.session_state.error_status:
    with st.container(border=True):
        st.header(st.session_state.error)


# Step 2: Show the rest of the page

# Layout logistics

# There is a conditional statement. Depending on the number of the st.session_state.page value different assets will be generated.
# Each asset however needs their own quick name to be identified.

# Except page 1 every page needs a valid user to be signed in. Pages 1 and 2 are the only pages that don't require a status to be made by the user and page 6 needs a valid recommendation number.
# The above conditions are initialised in Part B Step 4 every time the page loads.

# From now on any button needs a distinct key, it will be found as the key="XXX" in the button parameters, input fields are the same
# Buttons have other parameters like on_click= XXXXX is the function called when the button is clicked or args = [XXXXX, YYYYY] are the parameters of the function

# Text can be show either by a streamlit option, st.write/header/title... or use html in st.markdown. Both are utilised here.

# Users enter information is text fields, number fields, checkboxes and radio buttons.
# Text fields need to get information when the user presses enter, number fields need limits, checkboxes will return True or False and radio buttons will have a preselected choice unless specified.
# Each type of text input prompt will tell the user what to do to save their answer, thought it might be small in letters.

# Any command st. is a streamlit layout asset. Any command that starts with 'with XXXXX' will put the assets under it in the asset.
# Here that is used to put things in columns and putting things in a square.

# Database collection function
# When a user wants to delete and entry in any collection the Record Collection makes a new entry
# Record Collection keeps other things recorded as well and assigns a letter in an action
# Question Collection records every prompt the user enters as a question
# A tag with the same Recommendation ID, Title and Category will not be entered twice
# Look at the mongo file for more information

# Warning
# The database and the variable names refer to recommendations.
# The texts shown to the user use the word task

# The several pages are separated into files and called under the layout function in each, see files page_{Number} for the notes in each

insert_data()  # Insert default data if needed

if st.session_state.page == 1:  # 1 is the page where the user makes a new account or signs in with their passcode

    from page_1 import layout

    layout()

elif st.session_state.page == 2:  # 2 is the page where the user can answer questions about stress levels

    from page_2 import layout_2

    layout_2()

else:

    from menu import menu_layout

    menu_layout()

    if st.session_state.page == 3:  # 3 is the home page where the user can see and complete recommendations

        from page_3 import layout_3

        layout_3()

    elif st.session_state.page == 4:  # 4 is the profile and preferences page where the user can update their profile and manage their preferences

        from page_4 import layout_4

        layout_4()

    elif st.session_state.page == 5:  # 5 is the Record page where the user can see their application history

        from page_5 import layout_5

        layout_5()

    elif st.session_state.page == 6:  # 6 is the page where the user can see a recommendation in full

        from page_6 import layout_6

        layout_6()

    elif st.session_state.page == 7:  # 7 is the tutorial page where the user can see how the application works

        from page_7 import layout_7

        layout_7()

    elif st.session_state.page == 8:  # 8 is the page where the user can make a confession and manage their confessions

        from page_8 import layout_8

        layout_8()

    elif st.session_state.page == 9:  # 9 is the page where an admin can add entries to the collections of the database

        from page_9 import layout_9

        layout_9()

    elif st.session_state.page == 10:  # 10 is the evaluation page where the admin can do the evaluation

        from page_10 import layout_10

        layout_10()

    else:

        # If for any reason a number more than 9 is called we show message with the number
        # This should never realistically happen

        st.write('You are on page ', st.session_state.page)
