from datetime import datetime
from mongo_connection import User
from check_and_balance import new_entry_in_record_collection, new_entry_in_score_history_collection


# This function gets a passcode given and finds if it is attached to user, if so it will sign them in
def validate_user(passcode):
    # The function has 2 returns
    # One is a message of the outcome of the function and the other is True/False
    # True means the function completed its task: finding a user that matches the passcode given

    if not passcode.strip():
        # The user will need to have entered a passcode the isn't empty

        return False, "You need to enter your passcode"

    user = User.find_one({"Passcode": passcode})  # Find the user using their Passcode

    if user is None:
        return False, "You do not have an account"

    new_entry_in_record_collection(passcode, f"User {passcode} signed in.", "P")  # Make a record of the user signing in

    return True, "You have an account"


# This function will create a user if given the right data for them
def new_user(username, passcode, age, focus_area, time_available, suggestions, gender):
    # The function has 2 returns
    # One is a message of the outcome of the function and the other is True/False
    # True means the function completed its task: creating a new user and adding them to the collection for users

    if not username.strip() or passcode == "Please reload the page" or not age.strip() or not focus_area or time_available == 0 or suggestions == 0 or not gender.strip():
        # The user can't be created without all of their information being correct and appropriate
        # Some will just need to have value others will need to have appropriate value
        # Because these come from a streamlit input field, there have been limits placed to make sure the value in appropriate
        # The 'passcode == "Please reload the page" refers to the rare case where a passcode wasn't generated
        # To sum up the possibility of this conditions being found is very rare

        return False, "You need to fill in all fields provided to proceed. If Passcode not available reload the page."

    # Username and Passcode needs to be unique. These are uniquely generated initially, but we check just in case
    if User.find_one({
            "Username": username}):  # Since the user can change the username given to them this might be true, so we need to check the username is unique

        return False, "You need to enter a unique username"

    if User.find_one({
            "Passcode": passcode}):  # The passcode isn't available to the user, so we just need to make sure a user didn't register with the generated passcode

        return False, "Something went wrong, please reload the page and try again"

    User.insert_one(

        # Bellow we create the new user. Some information is given by the user, some is entered as defaulted

        {
            'Username': username,
            'Passcode': passcode,
            'Repeat_Preference': 1,
            # Not initially available for change by the user. This number will show the number of days the user won't see a recommendation twice
            'Age_Category': age,  # Age is a category ranging between 2 number, not a number specifically
            'Gender': gender,
            'Focus_Area': [str(item) for item in focus_area],
            'Suggestions': int(suggestions),
            # The number of suggestions to be picked are dependent of the number of available recommendation
            'Time_Available': time_available,
            'Level': 1,  # Not initially available for change by the user
            'Score': 0,  # Not initially available for change by the user
            'Streak': 0,  # Not initially available for change by the user
            'Days_Summed': 0,  # Not initially available for change by the user
            'Role': 'User',
            # Not initially available for change by the user. This opens up certain privileges for the right roles
            'Created_At': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

    )

    new_entry_in_score_history_collection(passcode)

    new_entry_in_record_collection(passcode,
                                   f"User {passcode} created their profile: Username {username}, Repeat Preference {1}, Age {age}, focus {focus_area}, suggestions {suggestions}, time available {time_available}, gender {gender}",
                                   "P")  # Make a record of the user setting up their profile

    new_entry_in_record_collection(passcode, f"User {passcode} has had their score set to 0",
                                   "S")  # Make a record of the user signing in

    return True, "You have been added to our service"
