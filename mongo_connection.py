from datetime import datetime, timedelta
import random
import pymongo
import streamlit as st
from Tables import Users, Tags, Recommendations
from langchain_community.llms import HuggingFaceHub


@st.cache_resource
def init_connection():
    return pymongo.MongoClient(st.secrets["mongo"][
                                   "uri"])  # Establish Connection with database using the url given by the server in the secrets file


client = init_connection()  # Establish Connection with database using the url given by the server in the secrets file

db = client.StressTest  # Find and define the database itself

# Find the various tables in the database, you will find the name of the collection in the db["XXX"] command
# Each one will have a structured entry that will be explained later
# For now keep in mind that every entry in every collection will include a time stamp of when it was created ('Created_At') and a user passcode ('Passcode')

Status = db["Status"]  # Keeps a rating of the user's stress

User = db["User"]  # Keeps the user information for every user

Question = db["Question"]  # Keeps record for each question was given to a user and answer the user gave

Record = db[
    "Record"]  # Keeps record for actions and changes to the user information that happens once a day or a week + other requests the user has made and changes in the database done by the user


# Here we have the function that inserts an entry in a record collection
def new_entry_in_record_collection(passcode, action, letter):
    # Each entry has 3 attributes that combined will identify the entry in the collection: Passcode, Type and Created_At
    # While Passcode and Type are used usually to track whether an action has already been done, so it isn't done twice
    # Type is a letter assigned to the type of action. While Action is more detailed Type is a letter:

    # Type A is for when a user's continuous days connected is increased or reset
    # Type B is for when a user's summed days connected are increased
    # Type D is for when a user's score is reset to 0 after a level evaluation
    # Type H is for when a user creates their profile
    # Type I is for when a user signs in with their passcode

    Record.insert_one(
        {
            'Passcode': passcode,  # The user passcode to find the user if needed
            'Action': action,  # Describing the action done in words
            'Type': letter,
            'Created_At': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    )

    # Find_Me


Recommendation_Per_Person = db[
    "Recommendation_Per_Person"]  # Keep a record for recommendations given to a user as paired by a status made by the user

Tag = db["Tag"]  # Will give a category of a criteria to keep users that wouldn't match a recommendation

Recommendation = db["Recommendation"]  # Will have potential recommendations to show a user


# Here we have a function that will insert the default data
def insert_data():
    # Fill the database with the default data as established by the table file, with safeguards to avoid adding the twice

    if not User.find_one({"Username": "Admin"}):  # Will initialise collection User with default data

        User.insert_many(Users)

    if not Tag.find_one({"ID": 1}):  # Will initialise collection Tag with default data

        Tag.insert_many(Tags)

    if not Recommendation.find_one({"ID": 1}):  # Will initialise collection Recommendation with default data

        Recommendation.insert_many(Recommendations)


Removed_Recommendation = db[
    "Removed_Recommendation"]  # Will have a record for recommendations a user rejected to avoid giving it to them again

Favorite_Recommendation = db[
    "Favorite"]  # Will have a record for recommendations a user liked, so they can see them again

Question_Questionnaire = db[
    "Questionnaire"]  # Will have the questioner questions to be shown and a user can rate their stress level

Score_History = db[
    "Score_History"]  # Keeps a record for the user's score history to create a chart showing the changes of the score

llm = HuggingFaceHub(repo_id="mistralai/Mistral-7B-Instruct-v0.2",
                     huggingfacehub_api_token="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")  # Initialize the LLM


# Here we will return the collections to be used in the application, this happens here to take away the need to double the connection code on another file
def return_collections():
    return User, Recommendation, Tag, Question_Questionnaire, Score_History, Question, Status


# Here we have a function the inserts an entry in the score history collection
def new_entry_in_score_history_collection(passcode):
    # The collection keeps a user Passcode and a time stump. These are the keys that identify the entry in the collection
    # It also keeps an 'Outcome' that shows whether the user would pass with the score to the next level.
    # To calculate the outcome we find the user based on a passcode, get the passing / demoting score and compare

    user = User.find_one({"Passcode": passcode})  # Find the user using their Passcode  # Find the user

    up, down = get_limits(user['Level'])  # Find the limits

    # Calculate the outcome

    outcome = None

    if user['Score'] > up:
        outcome = True

    if user['Score'] < down:
        outcome = False

    # Other than that it keeps the user's score and level at the time ('Score') and ('Level').

    Score_History.insert_one(
        {
            'Passcode': passcode,
            'Score': user['Score'],
            'Level': user['Level'],
            'Outcome': outcome,
            'Created_At': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    )


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

    new_entry_in_record_collection(passcode, f"User {passcode} signed in.", "I")  # Make a record of the user signing in

    return True, "You have an account"


# This function will create a user if given the right data for them
def new_user(username, passcode, age, focus_area, time_available, suggestions):
    # The function has 2 returns
    # One is a message of the outcome of the function and the other is True/False
    # True means the function completed its task: creating a new user and adding them to the collection for users

    if not username.strip() or passcode == "Please reload the page" or not age.strip() or not focus_area.strip() or time_available == 0 or suggestions == 0:
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
            'Focus_Area': focus_area,
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
                                   f"User {passcode} created their profile: Username {username}, Repeat Preference {1}, Age {age}, focus {focus_area}, suggestions {suggestions}, time available {time_available}",
                                   "H")  # Make a record of the user setting up their profile

    new_entry_in_record_collection(passcode, f"User {passcode} has had their score set to 0",
                                   "D")  # Make a record of the user signing in

    return True, "You have been added to our service"


# This function generates a unique passcode, a 10-digit number that isn't in any collection to make sure no confusions happen
def generate_unique_passcode():
    attempt_count = 0

    # Bellow is the names of collections in the database in a table

    all_collections = [
        "Status", "User", "Question", "Record", "Recommendations_Per_Person",
        "Tag", "Recommendation", "Removed_Recommendation", "Favorite_Recommendation"
    ]

    while attempt_count < 100:

        passcode = str(random.randint(1000000000, 9999999999))  # Generate 10 digit number

        passcode_exists = False

        for collection_name in all_collections:  # Go through all the collections to find the number

            collection = db[collection_name]  # Get the collection using the table above to get the name

            if collection.find_one({"Passcode": passcode}):
                passcode_exists = True

                break

            if not passcode_exists:
                return passcode

        attempt_count += 1

    return "Please reload the page"  # The algorithm has 100 chances to find a unique number, failing that it sends a message to reload the page and try again


# This function generates a unique username for a user, the user can change it, but it starts like this 
def generate_animal_username(max_attempts=100):
    attempt_count = 0

    # The tables will be a mix and match of names to make the username
    animals = ['Lion', 'Tiger', 'Elephant', 'Giraffe', 'Zebra', 'Panda', 'Koala', 'Kangaroo', 'Cheetah', 'Penguin']
    adjectives = ['Fluffy', 'Mighty', 'Sneaky', 'Grumpy', 'Mysterious', 'Sleepy', 'Bold', 'Spiky', 'Shiny', 'Wild']

    while attempt_count < max_attempts:

        username = f"{random.choice(adjectives)}{random.choice(animals)}#{random.randint(1000, 9999)}"  # The username is 2 words from the tables above and a 4-digit number

        if not User.find_one({
                                 "Username": username}):  # Unlike the Passcode the username is only stored in the User Collection, so we only need to check in this table

            return username  # If we can't find the generated username we submit it

        attempt_count += 1

    return "Please reload the page"  # The algorithm has 100 chances to find a unique number, failing that it sends a message to reload the page and try again


# This function records a question and an answer the user has given
def record_question(question, answer, passcode, function=None):

    # The function has 2 returns
    # One is a message of the outcome of the function and the other is True/False
    # True means the function completed its task: recording the question/answer 

    # The last parameter 'function' is rarely given and is here because 1, only 1, action in the application will have an additional filter to make sure the question needs to be recorded
    # It's a disclaimer and there isn't a middle function to weed out the unfit entries
    # Usually the function will be called when the data have already been verified

    if function is not None:  # The fact the function isn't None means we also need to check before entering the question in

        if not answer.strip() or not question.strip() or function is False:
            return False, "Question failed to be recorded"

    # This entry includes 4 attributes
    # The key attributes to seperate this entry in the Question collection can vary
    # To completely seperate each entry use: 
    # The Passcode, the unique user passcode of the user that submitted the question
    # The description of the question
    # The timestamp of when the entry was created

    Question.insert_one(
        {
            'Passcode': passcode,
            'Question': question,
            'Answer': answer,
            'Created_At': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    )

    return True, "Question recorded"


# This function finds the latest entry the user made to the Daily Stress Questioner and return several results
def get_status(passcode):
    latest_status = Status.find_one({"Passcode": passcode}, sort=[("Created_At",
                                                                   -1)])  # By only getting a passcode we find the last entry the user made to the Daily Stress Questioner

    if not latest_status:
        return False, False, -1  # The function returns 3 results, if the user has made no entry to the Daily Stress Questioner then we need to return some null entries

    last_status_time = datetime.strptime(latest_status['Created_At'],
                                         '%Y-%m-%d %H:%M:%S')  # Format the timestamp of the last user entry to compare

    now = datetime.now()

    # We return 3 results
    # First whether this last entry was done today - that means the user won't need to reenter the Daily Stress Questioner
    # If not and the user needs to enter the Daily Stress Questioner again we check whether the last entry was done yesterday
    # Then finally we return the ID of the latest entry of the Daily Stress Questioner, so we can later locate it

    return (now.date() == last_status_time.date()), ((now.date() - last_status_time.date()).days == 1), latest_status[
        "_id"]


# This function records the stress level of a user when given a Passcode and a number
def record_status(passcode, stress_level):
    # The function has 2 returns
    # One is a message of the outcome of the function and the other is True/False
    # True means the function completed its task: recording the stress level of the user

    if stress_level == -1:

        return False, "You need to fill in all fields provided to proceed"  # If for any reason the number is less than 0 (impossible) we send the message

    else:

        if not User.find_one({"Passcode": passcode}):
            return False, "Something went wrong, user not registered."  # Make sure the user is registered first - another thing that probably won't happen since this function won't be called then

        # This is a simple collection that only includes a Passcode of a user, a timestamp and the stress level of the user
        # We can use the passcode and the timestamp that will seperate each entry

        Status.insert_one(
            {
                'Passcode': passcode,
                'Stress_Level': stress_level,
                'Created_At': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        )

        return True, "Status recorded"


# This function checks and will increase the continuous days connected for a user, as given by a Passcode
def update_user_streak(passcode):
    # This function returns a message for the outcome of the function to show the user

    # As mentioned, user records are identified by letter that means a kind of action
    # Type B is days connected increased, so we need to check if we have done this daily action already

    last_record = Record.find_one({"Passcode": passcode, "Type": "B"}, sort=[("Created_At", -1)])

    if last_record:  # If there was a type B action made for the user we need to make sure it didn't happen today

        # Format the timestamp of the last action B to get the date and compare it with today

        last_time = datetime.strptime(last_record["Created_At"], "%Y-%m-%d %H:%M:%S")
        now = datetime.now()

        if last_time.date() == now.date():
            return "You have already signed in today, your streak will not change."

    if not User.find_one({"Passcode": passcode}):
        return "Something went wrong, user not registered."  # Make sure the user is registered first - another thing that probably won't happen since this function won't be called then

    User.update_one({"Passcode": passcode},
                    {"$inc": {"Days_Summed": 1}})  # We need to increase the days connected for the user anyway

    # Find the last status the user made (look in the function for more) and make sure we enter the right amount if return variables

    today, yesterday, index = get_status(passcode)

    if yesterday:

        User.update_one({"Passcode": passcode}, {
            "$inc": {"Streak": 1}})  # yesterday means the user was here yesterday, so we increase their streak

        message = "Your streak was increased."  # Custom a message for the user

        streak_action = f"Streak increased for user {passcode}"  # Custom the action done for the streak

    else:

        User.update_one({"Passcode": passcode}, {
            "$set": {"Streak": 1}})  # Since we are here the user wasn't here yesterday so the streak was reset

        if index == -1:

            message = "Wellcome to your first Status."  # Custom a message for the user

        else:

            message = "You did not check in less than 48 hours ago. Your streak was reset."  # Custom a message for the user

        streak_action = 'Streak reset'  # Custom the action done for the streak

    new_entry_in_record_collection(passcode, streak_action, 'A')

    new_entry_in_record_collection(passcode, f"Days connected increased for user {passcode}", 'B')

    return message


# This function calculates the amount of times an algorithm can fail to find an appropriate recommendation for a user depending on the amount of recommendations available
def calculate_fail_count():
    number_of_recommendations_in_total = Recommendation.count_documents(
        {})  # Step 1: Get the current number of recommendations in the Database

    total_possible_IDs = Recommendation.find_one({}, sort=[('ID', -1)])[
        'ID']  # Step 2: Get the ID of the last entered recommendation

    number_of_recommendation_after_removing_deleted_entries = total_possible_IDs - number_of_recommendations_in_total  # Step 3: Find the actual amount of recommendations by subtracting the biggest ID with the number of recommendations

    # The recommendations come with IDs from 1 and up
    # With deleted entries the IDs might go 1, 2, 4, 5
    # When a new recommendation is added the ID is set at the amount or recommendations + 1

    # Step 4: Return the appropriate amount of fails based of all of the above
    # We add 2 because when there are not deleted entries in the answer is 1, and we want to add some margin of error

    return (int(total_possible_IDs / (
                number_of_recommendations_in_total - number_of_recommendation_after_removing_deleted_entries))) + 2


# This function uses the function above to generate a valid recommendation ID, aka an ID that exists
def generate_valid_index():

    recommendation_fail = 0

    # We pick a random number between 1 and the amount of available recommendations
    # This works because the last recommendation added will have the biggest ID

    potential_recommendation_index = random.randint(1, Recommendation.count_documents({}))

    while Recommendation.find_one(
            {"ID": potential_recommendation_index}) is None and recommendation_fail <= calculate_fail_count():
        recommendation_fail += 1  # If the recommendation with the generated ID isn't found we add the fail count

        potential_recommendation_index = random.randint(1, Recommendation.count_documents({}))  # And we try again

    if recommendation_fail > calculate_fail_count():  # We use the above function to stop the algorithm form going in a look

        potential_recommendation_index = Recommendation.find_one({}, sort=[('ID', -1)])[
            'ID']  # In this case we pick the first available ID in the collection

    return potential_recommendation_index


# This function returns the amount of entries of the recommendations generated in 3 different ways, and a condition that tells us whether it run the entire function correctly
def calculate_entries(passcode):

    if not User.find_one(
            {"Passcode": passcode}):  # If we can't find the user we can't generate recommendations for them

        return False, 0, 0, 0

    entries_required = User.find_one({"Passcode": passcode})[
        'Suggestions']  # Find the user using their Passcode and get their number of preferences

    number_of_recommendations = Recommendation.count_documents({})  # Get the number of recommendations available

    if entries_required > number_of_recommendations:  # If required recommendations can't be satisfied by the available recommendations we return 0s

        return False, 0, 0, 0

    # There are 3 categories so when requiring 3 entries the answer is 1, 1, 1
    # But if the entries are less than 3 we have to manually return the right numbers

    if entries_required == 1:  # We need to have at least 1 entry generated by AI of if only one is required we only return 1 in the appropriate category

        return True, 0, 0, 1

    if entries_required == 2:  # If we require 2 we are adding one in the chosen by AI category

        return True, 0, 1, 1

    # The reason we give the least entries generated by AI is because we add the new entry in the database, and we don't want it to feel up

    # Get maximum possible entries (Your approach)

    max_entries_requested, additional_entries_via_button = get_maximum_entries()

    total_possible_entries = max_entries_requested + additional_entries_via_button

    # Start with max possible values

    entries_generated_by_AI = 1

    entries_chosen_by_Tags = int((total_possible_entries - entries_generated_by_AI) // 2)

    entries_chosen_by_algorithm = total_possible_entries - (entries_generated_by_AI + entries_chosen_by_Tags)

    # Reduce the numbers until we match entries_required

    excess_entries = total_possible_entries - entries_required

    index = 0  # Used for cycling through categories

    while excess_entries > 0:

        if index == 0 and entries_chosen_by_algorithm > 0:

            entries_chosen_by_algorithm -= 1

        elif index == 1 and entries_chosen_by_Tags > 0:

            entries_chosen_by_Tags -= 1

        excess_entries -= 1

        # Cycle through categories so no category disappears

        if index == 0:

            index = 1

        else:

            index = 0

    return True, entries_chosen_by_algorithm, entries_chosen_by_Tags, entries_generated_by_AI  # Return all 3 numbers


# This function generates a user profile to be added to a prompt to an AI, and a condition to indicate if it did it correctly
def generate_user_profile(passcode):
    user = User.find_one({"Passcode": passcode})  # Find the user using their Passcode

    if not user:  # If we can't find the user we can't generate recommendations for them

        return False, 'Something went wrong, user not registered'

    # Find the last status the user made (look in the function for more) and make sure we enter the right amount if return variables

    today, yesterday, index = get_status(passcode)

    if not today:  # If the user hasn't made a status, we can't generate a profile for them

        return False, 'Something went wrong, status was not found'

    stress_level = Status.find_one({"_id": index})['Stress_Level']  # Find the status to find the stress level

    answers = []  # Initialise table

    Question_Questionnaire_list = list(Question_Questionnaire.find())

    for entry in Question_Questionnaire_list:

        if Question.find_one({"Passcode": passcode, "Question": entry['Question']}, sort=[("Created_At", -1)]):

            answers.append(
                # The table will hold the latest answer to a questionnaire question, because wec can't long term give the AI all the answers long term
                {
                    'Question': entry['Question'],
                    'Answer': Question.find_one({"Passcode": passcode, "Question": entry['Question']}, sort=[("Created_At", -1)])['Answer']
                }
            )

    return True, f"User Age {user['Age_Category']} / User Focus Area {user['Focus_Area']} / User Time Available in Minutes {user['Time_Available']} / User Stress Level {stress_level} / User Latest Answers Related to Stress {answers} "


# This function generates a recommendation ID for a new recommendation to be added
def generate_recommendation_id():
    last_entry = Recommendation.find_one({},
                                         sort=[("ID", -1)])  # Step 1: Get the biggest ID in recommendation collection

    if last_entry:  # Step 2: Increase the biggest ID by one if there are recommendations, or set the new ID as 1

        generated_id = int(last_entry['ID']) + 1

    else:

        generated_id = 1

    while Recommendation.find_one({"ID": generated_id}) or Tag.find_one({"ID": generated_id}):
        generated_id += 1  # Step 3: Increase by 1 until the new id doesn't exist

    return generated_id


# This function adds a recommendation in the Recommendation collection, it returns an indicator that shows whether the function completed and a message
def add_recommendation(ID, passcode, title, description, link, points):
    ID = int(ID)  # Convert any possible IDs in text into numbers

    if not User.find_one(
            {"Passcode": passcode}):  # If we can't find the user we can add a recommendation on their behalf

        return False, "Something went wrong, user not registered"

    if Recommendation.find_one({"ID": ID}) or Tag.find_one(
            {"ID": ID}):  # If the ID matches any of the Tags or other Recommendations we can't add it

        return False, "Please try again, it look like the ID generated has already been added."

    if not title.strip() or not description.strip() or points < 10 or points > 150 or (
            link is not None and not link.strip()):
        return False, "You need to fill in all mandatory fields"  # Make sure the data entered are appropriate to be added

    # This collection's entries contain an ID that can be used as a key to find the entry across the collections
    # It also includes the passcode of the user that added it and a timestamp for when it was created
    # The content is a title, a description, a link that is optional and minimum points assigned to them

    Recommendation.insert_one(
        {
            'ID': ID,
            'Passcode': passcode,
            'Created_At': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'Title': title,
            'Description': description,
            'Link': link,
            'Points': points
        }
    )

    return True, "Recommendation added"


# This function adds a tag to a recommendation, it returns an indicator that shows whether the function completed and a message
def add_tag(ID, passcode, title, category):
    ID = int(ID)  # Convert any possible IDs in text into numbers

    if not User.find_one(
            {"Passcode": passcode}):  # If we can't find the user we can add a recommendation on their behalf

        return False, "Something went wrong, user not registered"

    if not Recommendation.find_one({"ID": ID}):  # We can't add a tag to a recommendation that doesn't exist

        return False, "Something went wrong, recommendation not found"

    if Tag.find_one({"ID": ID, "Title_Of_Criteria": title, "Category": category}):  # We can't add a tag twice

        return False, "Tag already exists"

    # This collection identifies an entry by 3 to maybe 4 attributes
    # The ID of the recommendation given this Tag, the criteria title and value (Category)
    # Other attributes that seperate an entry is a timestamp of creation and the passcode of the person that added it

    Tag.insert_one(
        {
            'ID': ID,
            'Passcode': passcode,
            'Title_Of_Criteria': title,
            'Category': category,
            'Created_At': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
    )

    return True, "Tag added"


# This function gets data to add a recommendation to a user to match it with a user status
def enter_recommendation_for_user(passcode, rec_id, fails, category):
    # Find the last status the user made (look in the function for more) and make sure we enter the right amount if return variables

    today, yesterday, index = get_status(passcode)

    status = Status.find_one({"_id": index})  # Find the status to find the timestamp

    user_recommendations = list(
        Recommendation_Per_Person.find({"Passcode": passcode, "Status_Created_At": status['Created_At']},
                                       sort=[("Pointer",
                                              1)]))  # Get all previous recommendations for the user's latest status

    # We will enter the new recommendation to the user with the below attributes:
    # The Passcode of the user
    # The ID of The recommendation
    # The Pointer is the row in which the recommendation was added
    # The Outcome is True if the recommendation hasn't been completed yet and False when it has
    # The Fail_Count shows if the recommendation was chosen and passed the various checks or was added because the program was on a loop 1/2 is passed the check and 3/2 is just added to avoid lopping
    # The limit is which we stop the looping is dictated by side function, look for the function for more
    # The timestamp of the status this pack of recommendations is assigned to. That with the passcode will direct towards to actual status in the Status Collection
    # Category will show how this recommendation was generated
    # A is for AI generated, B for AI chosen (B- if that method fails, and we have to pick manually again) and C for chosen by this program with no AI (C- if the recommendation didn't pass the tests but needed to be added anyway)
    # Category is for admin work and will not be seen by a user
    # Finally the timestamp of the entry, when it was created
    # To find an entry in this collection you need to Pointer, the Passcode and the Status timestamp
    # Another way is via the Passcode and the entry Timestamp, thought that is not always going to work

    Recommendation_Per_Person.insert_one(
        {
            'Passcode': passcode,
            'ID': rec_id,
            'Pointer': len(user_recommendations) + 1,
            'Outcome': True,
            'Fail_Count': f"{fails} / {calculate_fail_count()}",
            'Completed_At': None,
            'Status_Created_At': status['Created_At'],
            'Category': category,
            'Created_At': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    )


# This function generates a required amount of recommendations by setting a prompt in an openAI machine
def generate_recommendations_by_AI(passcode, entries_generated_by_AI, profile):

    user = User.find_one({"Passcode": passcode})  # Find the user using their Passcode

    # Find the last status the user made (look in the function for more) and make sure we enter the right amount if return variables

    today, yesterday, index = get_status(passcode)

    status = Status.find_one({"_id": index})  # Use the last result to find the status to get the stress level

    index = 0  # Set to the index to indicate we added a recommendation to the user to keep track of how many

    while index < entries_generated_by_AI:

        prompt = f"""User has profile {profile}. Generate (1) recommendation for relieving Stress."""  # Submit the prompt and get the response

        response = llm(prompt)  # Call the Hugging Face model to generate a response

        recommendation_generated_id = generate_recommendation_id()  # Generate an ID for a new recommendation in the Recommendation collection, this means that future users will be able to see this generated recommendation

        recommendation_added, recommendation_added_message = add_recommendation(recommendation_generated_id, "OpenAI",
                                                                                f"Recommendation number {recommendation_generated_id}",
                                                                                response, None,
                                                                                10)  # We enter OpenAI as the passcode of the creator

        fail_count = 0  # We have a minor fail count to keep track if the recommendation was added, we probably won't have to use it unless we have various users doing this at the same time

        while not recommendation_added and fail_count <= 100:  # We have a maximum of 100 attempts to enter the recommendations

            recommendation_generated_id = generate_recommendation_id()  # Generate an ID for a new recommendation in the Recommendation collection, this means that future users will be able to see this generated recommendation

            recommendation_added, recommendation_added_message = add_recommendation(recommendation_generated_id,
                                                                                    "OpenAI",
                                                                                    f"Recommendation number {recommendation_generated_id}",
                                                                                    response, None,
                                                                                    10)  # We enter OpenAI as the passcode of the creator

            fail_count += 1  # Increase the minor fail count

        if fail_count > 100 and not recommendation_added:

            enter_recommendation_for_user(passcode, generate_valid_index(), fail_count,
                                          'A-')  # Add the recommendation with Category A-, aka chosen by algorithm when is should have been generated by OpenAI

        else:

            # We add tags so this recommendation, so it will be shown to users equal and below the user's level
            # Tags usually restrict the recommendation from being seen by all the users, so use them sparingly and only if needed

            add_tag(recommendation_generated_id, "OpenAI", 'Age Variant', user['Age_Category'])

            add_tag(recommendation_generated_id, "OpenAI", 'Focus Area', user['Focus_Area'])

            add_tag(recommendation_generated_id, "OpenAI", 'Time Available', user['Time_Available'])

            add_tag(recommendation_generated_id, "OpenAI", 'Stress Level', status['Stress_Level'])

            add_tag(recommendation_generated_id, "OpenAI", 'Show for levels below', user['Level'])

            add_tag(recommendation_generated_id, "OpenAI", 'Show for levels equal', user['Level'])

            enter_recommendation_for_user(passcode, recommendation_generated_id, fail_count,
                                          'A')  # Add the recommendation with Category A, aka generated by OpenAI

        index += 1  # Increase to the index to indicate we added a recommendation to the user to keep track of how many

    return index


# This function generates a required amount of recommendations by establishing filters based on the various tags
def generate_recommendations_chosen_by_tags(passcode, entries_chosen_by_tags):

    tags = list(Tag.find())  # Gather the Tags for the recommendation to check

    user = User.find_one({"Passcode": passcode})  # Find the user using their Passcode

    # Find the last status the user made

    today, yesterday, index = get_status(passcode)

    status = Status.find_one({"_id": index})  # Use the last result to find the status to get the stress level

    filters = [  # Establish the filters as we are watering down the recommendation we are choosing from into the ones that match the tags
        {'Title_Of_Criteria': 'Age Variant', 'Category': user['Age_Category']},
        {'Title_Of_Criteria': 'Focus Area', 'Category': user['Focus_Area']},
        {'Title_Of_Criteria': 'Stress Level', 'Category': status['Stress_Level']},
        {'Title_Of_Criteria': 'Time Available', 'Category': user['Time_Available']},
        {'Title_Of_Criteria': 'Show for levels above', 'Category': user['Level']},
        {'Title_Of_Criteria': 'Show for levels below', 'Category': user['Level']},
        {'Title_Of_Criteria': 'Show for levels equal', 'Category': user['Level']},
    ]

    recommendations = []  # Set the recommendations table to keep the right recommendations

    pointer = 0  # The recommendation table is small and holds a number here and an ID

    user_recommendations = set()  # Track recommendations added to avoid duplicates

    for tag in tags:  # Loop to match tags with filters and gather valid recommendations

        for entry in filters:

            if entry['Title_Of_Criteria'] == tag['Title_Of_Criteria'] and entry['Category'] == tag['Category']:

                if Recommendation.find_one({'ID': tag['ID']}) and tag['ID'] not in user_recommendations:

                    recommendations.append({'ID': tag['ID'], 'Pointer': pointer})

                    user_recommendations.add(int(tag['ID']))  # Track recommendations added to avoid duplicates

                    pointer += 1

    fail_count = 0  # Set fail count to avoid loops

    index = 0  # Set counter to keep track of entries added

    user_recommendations.clear()  # Clear the user recommendations to hold the recommendations selected now

    # Handle recommendations depending on the number of results
    # If there are enough recommendations, fill the user slots by random selection and avoiding duplicates
    # Else load up all the availble and fill the rest by randomly generated  from all the recommendations not just the ones appropriate

    while index < entries_chosen_by_tags:

        if len(recommendations) <= entries_chosen_by_tags:

            # Fill with available recommendations

            for entry in recommendations:

                enter_recommendation_for_user(passcode, int(entry['ID']), calculate_fail_count() + 1, 'B-')  # Category B- means that while we selected a recommendation that was meant to be randomly selected by our recommendations, we had to add it in without selection

                user_recommendations.add(int(entry['ID']))  # Track recommendations added to avoid duplicates

                index += 1  # Increase to show that we added a recommendation

            # Fill remaining slots if there are not enough recommendations

            while index <= entries_chosen_by_tags:

                potential_recommendation_index = generate_valid_index()  # Generate a recommendation ID the exists

                index, fail_count, user_recommendations = validate_recommendation_pick(fail_count, index, passcode, potential_recommendation_index, user_recommendations, 'B-')  # Category B- means that while we selected a recommendation that was meant to be randomly selected by our recommendations, we had to add it in without selection

            break  # Exit the loop as we're done

        else:
            # More recommendations than needed, pick randomly without duplicates

            potential_recommendation_index = random.randint(1, pointer)

            index, fail_count, user_recommendations = validate_recommendation_pick(fail_count, index, passcode, potential_recommendation_index, user_recommendations, 'B')

    return index


# This function is here because the code below appeared twice in a function, it does some calculations with data and returns the new values
def validate_recommendation_pick(fail_count, index, passcode, potential_recommendation_index, user_recommendations, category):

    if potential_recommendation_index not in user_recommendations:  # User recommendation hold the recommendation already given, we can add a recommendation twice

        enter_recommendation_for_user(passcode, int(potential_recommendation_index), fail_count, category)  # Category will be B or B-. B- is explaied in the bigger function, B means the recommendation was selected randomly from a list of pre-approved recommendations

        user_recommendations.add(int(potential_recommendation_index))  # Track recommendations added to avoid duplicates

        index += 1  # Increase to show that we added a recommendation

        fail_count = 0  # Keeps us from looping forever, we set it back to 0

    else:

        fail_count += 1  # Keeps us from looping forever, we increased it because we failed to find it recommendation valid to add

    if fail_count > calculate_fail_count():

        potential_recommendation_index = generate_valid_index()

        enter_recommendation_for_user(passcode, potential_recommendation_index, fail_count, 'B-')  # Category B- means that while we selected a recommendation that was meant to be randomly selected by our recommendations, we had to add it in without selection

        user_recommendations.add(int(potential_recommendation_index))  # Track recommendations added to avoid duplicates

        index += 1  # Increase to show that we added a recommendation

        fail_count = 0  # Keeps us from looping forever, we set it back to 0

    return index, fail_count, user_recommendations


# This Function returns 2 things. The minimum limit for the recommendations a user can request when ending their information and the additional they can request via a button
def get_maximum_entries():
    return int(Recommendation.count_documents({}) / 4), int(Recommendation.count_documents({}) * 0.1)


# This function validates a recommendation in the filter of it not being given to the user in a set amount of days
def has_the_user_seen_this_recommendation_before(passcode, potential_recommendation_index):
    user = User.find_one({"Passcode": passcode})  # Find the user using their Passcode

    # The user has entered a repeat preference, aka the number of days they don't want to see a recommendation again
    # To do that we will check the recommendations per person collection where we store the recommendations given to a user

    return not Recommendation_Per_Person.find_one(
        {'Passcode': passcode, 'ID': potential_recommendation_index,
         'Created_At': {'$gte': datetime.now() - timedelta(days=user['Repeat_Preference'])}}
    )


# This function gets a recommendation ID and a user Passcode, it will check for tags to see if they match the user
def do_the_tags_match(passcode, potential_recommendation_index):

    tags = list(Tag.find({"ID": potential_recommendation_index}))  # Gather the Tags for the recommendation to check

    user = User.find_one({"Passcode": passcode})  # Find the user using their Passcode

    # Find the last status the user made (look in the function for more) and make sure we enter the right amount if return variables

    today, yesterday, index = get_status(passcode)

    status = Status.find_one({"_id": index})  # Use the last result to find the status to get the stress level

    for tag in tags:

        # There are 4 kinds of criteria as identified by the Title_Of_Criteria
        # Depending on them, we compare with the right attribute
        # We gather data from the user profile and the last status

        if tag['Title_Of_Criteria'] == 'Age Variant' and tag['Category'] != user['Age_Category']:
            return False

        if tag['Title_Of_Criteria'] == 'Focus Area' and tag['Category'] != user['Focus_Area']:
            return False

        if tag['Title_Of_Criteria'] == 'Stress Level' and int(tag['Category']) <= status['Stress_Level']:
            return False

        if tag['Title_Of_Criteria'] == 'Time Available' and int(tag['Category']) < user['Time_Available']:
            return False

        if tag['Title_Of_Criteria'] == 'Show for levels above' and int(tag['Category']) < user['Level']:
            return False

        if tag['Title_Of_Criteria'] == 'Show for levels below' and int(tag['Category']) > user['Level']:
            return False

        if tag['Title_Of_Criteria'] == 'Show for levels equal' and int(tag['Category']) != user['Level']:
            return False

    return True


# This function chooses and adds a recommendation to a user's list today
def generate_recommendation(passcode):

    if not User.find_one(
            {"Passcode": passcode}):  # If we can't find the user we can't generate recommendations for them

        return False, "Something went wrong, user not registered"

    if Recommendation.count_documents({}) == 0:  # If we don't have recommendations we can't return any to the user

        return False, 'There are no recommendations available for you.'

    # Find the last status the user made (look in the function for more) and make sure we enter the right amount if return variables

    today, yesterday, index = get_status(passcode)

    if not today:  # If the user hasn't made a status, we can't generate recommendations for them either

        return False, 'Something went wrong, status was not found'

    status = Status.find_one({"_id": index})  # Find the status to find the timestamp

    entries_requested, additional_entries_via_button = get_maximum_entries()

    if Recommendation_Per_Person.count_documents(
            {"Passcode": passcode, "Status_Created_At": status['Created_At']}) >= entries_requested + additional_entries_via_button:  # A user can't see the whole database daily, so we have limits
        return False, "You have received most available recommendations. No more for now!"

    user_recommendations = list(
        Recommendation_Per_Person.find({"Passcode": passcode, "Status_Created_At": status['Created_At']},
                                       sort=[("Pointer",
                                              1)]))  # Get all previous recommendations for the user's latest status

    fails = 0

    potential_recommendation_index = generate_valid_index()  # We have a function that will generate a valid recommendation ID - at least one that will exist

    while fails <= calculate_fail_count():  # We use max tries to avoid looping, we have another function to calculate that

        # To make sure we get the appropriate recommendation we will check various things:
        # Whether the recommendation was seen by the user before within a time period
        # Whether it will be a duplicate in this set
        # Whether the Tags class with the user
        # Whether the user rejected this recommendation before
        # If we fail one of the above we will add the fail count and try again with another ID

        if (
                has_the_user_seen_this_recommendation_before(passcode, potential_recommendation_index) and
                sum(1 for rec in user_recommendations if rec['ID'] == potential_recommendation_index) == 0 and
                do_the_tags_match(passcode, potential_recommendation_index) and
                Removed_Recommendation.find_one({"ID": potential_recommendation_index, "Passcode": passcode}) is None):

            enter_recommendation_for_user(passcode, potential_recommendation_index, fails,
                                          'C')  # Add the recommendation with Category C, aka chosen by algorithm and passing through various filters

            return True, "Recommendation added"

        else:

            fails += 1

            potential_recommendation_index = generate_valid_index()

    enter_recommendation_for_user(passcode, generate_valid_index(), fails, 'C-')

    return True, 'Recommendation added'


#  This function randomly chooses a recommendation for the user based of Tags and history
def generate_recommendations_by_algorithm(passcode,entries_chosen_by_algorithm):

    index = 0  # Set to the index to indicate we added a recommendation to the user to keep track of how many

    fail_count = 0  # We keep count of the failed attempts to avoid falling into loops. If we do fall in one we add an algorithm generated pick and add an - in the category to show

    while index < entries_chosen_by_algorithm:

        recommendation_added, recommendation_added_message = generate_recommendation(
            passcode)  # This side function is designed to break loops always add a valid recommendation to a user #

        if not recommendation_added:

            fail_count += 1  # We keep count of the failed attempts to avoid falling into loops. If we do fall in one we add an algorithm generated pick and add an - in the category to show

            if fail_count > calculate_fail_count():

                enter_recommendation_for_user(passcode, generate_valid_index(), fail_count,
                                              'C-')  # Add the recommendation with Category C-, aka chosen by algorithm without going through the filters

                recommendation_added = True

        if recommendation_added:  # # But just in case it ends prematurely it has a condition return that was can use to see if it was added

            index += 1  # Add to the index to indicate we added a recommendation to the user to keep track of how many

            fail_count = 0  # We keep count of the failed attempts to avoid falling into loops. If we do fall in one we add an algorithm generated pick and add an - in the category to show

    return index


# This function generates recommendations via varius methods for users
def get_recommendations(passcode):

    # The function has 3 returns
    # One is a message of the outcome of the function and the other is True/False
    # True means the function completed its task: generating recommendations for users as requested
    # It will also either return None or a dictionary list for the user that will be styled later

    if not User.find_one(
            {"Passcode": passcode}):  # If we can't find the user we can't generate recommendations for them

        return False, None, "Something went wrong, user not registered"

    if Recommendation.count_documents({}) == 0:  # If we don't have recommendations we can't return any to the user

        return False, None, 'There are no recommendations available for you.'

    # Find the last status the user made (look in the function for more) and make sure we enter the right amount if return variables

    today, yesterday, index = get_status(passcode)

    if not today:  # If the user hasn't made a status, we can't generate recommendations for them either

        return False, None, 'Something went wrong, status was not found'

    status = Status.find_one({"_id": index})  # Find the status to find the timestamp

    latest_recommendation = Recommendation_Per_Person.find_one({"Passcode": passcode}, sort=[
        ("Created_At", -1)])  # Get the last recommendation given to match with the status

    if latest_recommendation and status['Created_At'] == latest_recommendation['Status_Created_At']:
        # If matched that means recommendations have been gathered for the user, and we can return them instead

        return True, list(
            Recommendation_Per_Person.find({"Passcode": passcode, "Status_Created_At": status['Created_At']},
                                           sort=[("Pointer", 1)])), 'Feel free to try any of the below.'

    # Get the entries that will be generated by what method

    entries_calculated, entries_chosen_by_algorithm, entries_chosen_by_Tags, entries_generated_by_AI = calculate_entries(
        passcode)

    if not entries_calculated:  # If for any reason the function above didn't produce the right results, we end this early

        return False, None, 'Something went wrong, recommendations not able to be generated'

    profile_completed, profile = generate_user_profile(passcode)  # Generate user profile

    if not profile_completed:  # If for any reason the function above didn't produce the right results, we end this early

        return False, None, "Something went wrong, profile wasn't able to be generated"

    recommendations_given = 0

    recommendations_given += generate_recommendations_by_AI(passcode, entries_generated_by_AI, profile)

    recommendations_given += generate_recommendations_chosen_by_tags(passcode, entries_chosen_by_Tags)

    recommendations_given += generate_recommendations_by_algorithm(passcode,entries_chosen_by_algorithm)

    return True, list(
        Recommendation_Per_Person.find({"Passcode": passcode, "Status_Created_At": status['Created_At']},
                                       sort=[("Pointer",
                                              1)])), f"Feel free to try any of the {recommendations_given} tasks below."


# This function will get a timestamp and will be returning None, or a statement that describes the time since then
def get_time(timestamp):
    if timestamp is None:  # The timestamp is dependent on if the user has completed a recommendation, so it might not exist yet

        return None

    # Formal the timestamp, thought it was entered as a time stamp it got saved as a string
    # Then we get the difference from now

    time_diff = datetime.now() - datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")

    # Since we get the time difference we can seperate them in days, hours, minutes and seconds

    days = time_diff.days
    hours, remainder = divmod(time_diff.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    return f"{days} days, {hours} hours ago" if days > 0 else f"{hours} hours, {minutes} minutes and {seconds} seconds ago"


# This function gets the recommendations given to a user and structures a table with additional information
def make_recommendation_table(recommendations, passcode):
    # The function has 2 returns
    # One is a boolean condition that will be True if the function reaches the end without failing out for some reason
    # The other is a None, or a dictionary table that mixes the Recommendation_Per_Person collection with the Recommendation collection

    if not User.find_one({"Passcode": passcode}):  # If we can't find the user we can't work the data

        return False, None

    Recommendation_table = []  # Create the table to fill and return later

    for entry in recommendations:  # Recommendations is the Recommendations given to user today

        this_recommendation = Recommendation.find_one({"ID": entry[
            'ID']})  # To not keep unneeded information wi only stored the recommendation ID, so we need to search for the ID in the recommendation collection to get the description/title

        if not this_recommendation:  # If for any reason a recommendation that doesn't exist we end prematurely

            return False, None

        # The new mixed table has the below fields:
        # From the Recommendations_Per_Person we keep the ID, the Pointer, the Outcome (will tell us if we will show the Done button or not)
        # The Timestamp of the status this recommendation was added to the user for, and then a statement as to how long ago the recommendation was completed
        # From the Recommendation we have the Title, Description and Points assigned (Points given will depend on the user's level)
        # The Preference is True, False or None. This indicates that the recommendation was found in the user's favorites (True), Removed (False) or has no characterisation (None)

        new_entry = [  # Construct the new entry and add it in the table
            {
                'ID': entry['ID'],
                'Pointer': entry['Pointer'],
                'Outcome': entry['Outcome'],
                'Status_Created_At': entry['Status_Created_At'],
                'Completed_At': get_time(entry['Completed_At']),
                'Title': this_recommendation['Title'],
                'Description': this_recommendation['Description'],
                'Points': this_recommendation['Points'],
                'Preference': (
                    False if Removed_Recommendation.find_one({"ID": entry['ID'], "Passcode": passcode})
                    else True if Favorite_Recommendation.find_one({"ID": entry['ID'], "Passcode": passcode})
                    else None
                )
            }
        ]

        Recommendation_table.extend(new_entry)

    return True, Recommendation_table


# This function gets a level and will calculate the limit score of the level.
def get_limits(level):  # Start here

    x = 100 * level
    y = 50 - 5 * level

    move_up_threshold = x * level
    move_down_threshold = move_up_threshold * (1 - y / 100)

    return move_up_threshold, move_down_threshold


# Main page function
def get_record(passcode):
    if not User.find_one({"Passcode": passcode}):
        return False
    today = datetime.today().date()
    week_start = today
    if not today.weekday() == 0:
        week_start = today - timedelta(days=today.weekday())
    return Record.find_one({"Passcode": passcode, "Type": "D",
                            "Created_At": {"$gte": week_start.isoformat()}}) is None and Status.count_documents(
        {"Passcode": passcode}) > 1


# Main Page Function
def determine_level_change(passcode):
    if not User.find_one({"Passcode": passcode}):
        return "Something went wrong, user not registered"
    user = User.find_one({"Passcode": passcode})  # Find the user using their Passcode
    move_up_threshold, move_down_threshold = get_limits(user['Level'])
    message_for_user = f"You have remained at level {user['Level']}."
    message_for_system = f"User remained at level {user['Level']}."
    if user["Score"] > move_up_threshold:
        User.update_one({"Passcode": passcode}, {"$inc": {"Level": 1}})
        user = User.find_one({"Passcode": passcode})  # Find the user using their Passcode
        message_for_user = f"You have moved up to level {user['Level']}."
        message_for_system = f"User {passcode} moved up to level {user['Level']}"
    elif user["Score"] < move_down_threshold:
        if user["Level"] != 1:
            User.update_one({"Passcode": passcode}, {"$inc": {"Level": -1}})
            user = User.find_one({"Passcode": passcode})  # Find the user using their Passcode
            message_for_user = f"You have been demoted to level {user['Level']}."
            message_for_system = f"User {passcode} has been demoted to level {user['Level']}"
        else:
            message_for_user = "You have been demoted but remained at level 1."
            message_for_system = f"User {passcode} was demoted but remained at level 1"
    User.update_one({"Passcode": passcode}, {"$set": {"Score": 0}})
    Score_History.insert_one(
        {
            'Passcode': passcode,
            'Score': user["Score"],
            'Level': user["Level"],
            'Outcome': False,
            'Created_At': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    )
    Record.insert_many(
        [
            {
                'Passcode': passcode,
                'Action': message_for_system,
                'Type': "C",
                'Created_At': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            },
            {
                'Passcode': passcode,
                'Action': f"User {passcode} has had their score set to 0",
                'Type': "D",
                'Created_At': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        ]
    )
    return message_for_user


# Main page function
def add_points(index, passcode, status):
    user = User.find_one({"Passcode": passcode})  # Find the user using their Passcode
    if not user:
        return False, "Something went wrong, user not found"
    recommendation = Recommendation.find_one({"ID": index})
    if not recommendation:
        return False, "Something went wrong, Recommendation not found"
    recommendation_per_person_entry = Recommendation_Per_Person.find_one(
        {"ID": index, "Passcode": passcode, "Status_Created_At": status})
    if not recommendation_per_person_entry:
        return False, "Something went wrong, Recommendation not found in given recommendations"
    up, down = get_limits(user['Level'])
    points = user['Level'] * recommendation['Points']
    if user['Score'] + user['Level'] * recommendation['Points'] <= up + 50:
        User.update_one({"Passcode": passcode}, {"$inc": {"Score": user['Level'] * recommendation['Points']}})
    else:
        User.update_one({"Passcode": passcode}, {"$set": {"Score": up + 50}})
        points = up + 50 - user['Score']
    Recommendation_Per_Person.update_one({"ID": index, "Passcode": passcode, "Status_Created_At": status}, {
        "$set": {"Outcome": False, "Completed_At": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}})
    new_entry_in_score_history_collection(passcode)
    Record.insert_many(
        [
            {
                'Passcode': passcode,
                'Action': f"User {passcode} increased their score by {points} points",
                'Type': "E",
                'Created_At': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            },
            {
                'Passcode': passcode,
                'Action': f"User {passcode} completed recommendation {index}",
                'Type': "F",
                'Created_At': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        ]
    )
    return True, f"User {passcode} increased their score by {points} points"


# Main page function
def change_recommendation_preference_for_user(preference, passcode, index, function=None):
    if User.count_documents({"Passcode": passcode}) == 0:
        return False, "Something went wrong, user not found"
    if Recommendation.count_documents({"ID": index}) == 0:
        return False, "Something went wrong, Recommendation not found"
    Favorite_Recommendation.delete_one({"ID": index, "Passcode": passcode})
    Removed_Recommendation.delete_one({"ID": index, "Passcode": passcode})
    if function is True:
        return True, "Task Completed"
    new_entry = {
        'Passcode': passcode,
        'ID': index,
        'Created_At': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    if preference == -1:
        Removed_Recommendation.insert_one(new_entry)
    else:
        Favorite_Recommendation.insert_one(new_entry)
    return True, "Task Completed"


# User profile page (for user) function
def update_user(passcode, username, repeat, age, focus_area, time_available, suggestions):
    user = User.find_one({"Passcode": passcode})  # Find the user using their Passcode
    if not user:
        return False, "Something went wrong, user not registered"
    if User.find_one({"Username": username}) and username != user['Username']:
        return False, "You need to enter a unique username"
    if not focus_area.strip() or time_available == 0 or suggestions == 0 or repeat == 0 or not age.strip():
        return False, "You need to enter appropriate information"
    User.update_one({"Passcode": passcode}, {"$set": {
        "Username": username,
        "Repeat_Preference": repeat,
        "Age_Category": age,
        "Focus_Area": focus_area,
        "Suggestions": suggestions,
        "Time_Available": time_available
    }})
    Record.insert_one(
        {
            'Passcode': passcode,
            'Action': f"User {passcode} updated their profile: Username {username}, Repeat Preference {repeat}, Age {age}, focus {focus_area}, suggestions {suggestions}, time available {time_available}",
            'Type': "G",
            'Created_At': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    )
    return True, "User Profile Updated"


# Recommendation page (for user) side function
def add_collection(passcode, status, collection_name, collection, completed):
    if not status:
        return None
    data_table = []
    data = collection.find({"Passcode": passcode})
    for entry in data:
        outcome = None
        if collection == Recommendation_Per_Person:
            outcome = entry['Outcome']
        if (collection == Recommendation_Per_Person and (
                outcome == completed or completed is None)) or collection != Recommendation_Per_Person:
            data_table.extend(create_entry(entry['ID'], passcode, collection_name, outcome, entry['Created_At']))
    return data_table


# Recommendation page (for user) side function    
def create_entry(index, passcode, collection, outcome, created):
    this_recommendation = Recommendation.find_one({"ID": index})
    if this_recommendation:
        new_entry = [
            {
                'Title': this_recommendation['Title'],
                'Description': this_recommendation['Description'],
                'ID': index,
                'Type': collection,
                'Outcome': outcome,
                'Created_At': created,
                'Extend': True,
                'Remove': (
                    True if Removed_Recommendation.find_one(
                        {"ID": this_recommendation['ID'], "Passcode": passcode}) or Favorite_Recommendation.find_one(
                        {"ID": this_recommendation['ID'], "Passcode": passcode})
                    else False
                )
            }
        ]
    else:
        new_entry = [
            {
                'Title': "Recommendation not found",
                'Description': "Recommendation not found",
                'ID': "Recommendation not found",
                'Type': collection,
                'Outcome': outcome,
                'Created_At': created,
                'Extend': False,
                'Remove': False
            }
        ]
    return new_entry


# Recommendation page (for user) side function
def sort_by_created_by(entry):
    return entry["Created_At"]


# Recommendation page (for user) function
def create_recommendation_history(passcode, order, include_favorite, include_removed,
                                  include_Recommendations, completed):
    user = User.find_one({"Passcode": passcode})  # Find the user using their Passcode
    query = f"Order: {order} - Favorite {include_favorite} - Removed {include_removed} - Per Person {include_Recommendations} / {completed}"
    if not user:
        return False, None, "Something went wrong, user not registered"
    user_recommendation = []
    temporary_table = add_collection(passcode, include_favorite, "Favorite_Recommendation", Favorite_Recommendation,
                                     None)
    if temporary_table is not None:
        user_recommendation.extend(temporary_table)
    temporary_table = add_collection(passcode, include_removed, "Removed_Recommendation", Removed_Recommendation, None)
    if temporary_table is not None:
        user_recommendation.extend(temporary_table)
    temporary_table = add_collection(passcode, include_Recommendations, "Recommendation_Per_Person",
                                     Recommendation_Per_Person, completed)
    if temporary_table is not None:
        user_recommendation.extend(temporary_table)
    user_recommendation.sort(key=sort_by_created_by, reverse=(order == -1))
    Record.insert_one(
        {
            'Passcode': passcode,
            'Action': f"User {passcode} requested record for {query}",
            'Type': "L",
            'Created_At': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    )
    return True, user_recommendation, f"Record for user {passcode} assembled."


# Questionnaire page (for admin) function
def add_question_to_Questionnaire(ID, passcode, question_input):
    ID = int(ID)
    if not User.find_one({"Passcode": passcode}):
        return False, "Something went wrong, user not registered"
    if Question_Questionnaire.find_one({"ID": ID}):
        return False, "ID already exists"
    if Question_Questionnaire.find_one({"Question": question_input}):
        return False, "Question already exists"
    if not question_input.strip():
        return False, "You need to enter a question"
    Question_Questionnaire.insert_one(
        {
            'ID': ID,
            'Passcode': passcode,
            'Question': question_input,
            'Created_At': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
    )
    return True, "Question added"


# Database page (for admin) function
def delete_entry(passcode, key, key2, created, collection_name, this_user_passcode):
    if not User.find_one({"Passcode": passcode}):
        return False, "Something went wrong, requested user not registered"
    if not User.find_one({"Passcode": this_user_passcode}):
        return False, None, "Something went wrong, User not registered"
    if collection_name == "User":
        query = {"Passcode": passcode}
    elif collection_name == "Question":
        query = {"Passcode": passcode, "Question": key, "Created_At": created}
    elif collection_name == "Record":
        query = {"Passcode": passcode, "Type": key, "Created_At": created}
    elif collection_name == "Status":
        query = {"Passcode": passcode, "Created_At": created}
    elif collection_name == "Recommendation":
        query = {"ID": key, "Created_At": created}
    elif collection_name == "Tag":
        query = {"Passcode": passcode, "ID": key, "Category": key2, "Created_At": created}
    elif collection_name == "Favorite_Recommendation":
        query = {"Passcode": passcode, "ID": key, "Created_At": created}
    elif collection_name == "Removed_Recommendation":
        query = {"Passcode": passcode, "ID": key, "Created_At": created}
    elif collection_name == "Recommendation_Per_Person":
        query = {"Passcode": passcode, "Pointer": key, "ID": key2, "Created_At": created}
    elif collection_name == "Question_Questionnaire":
        query = {"Passcode": passcode, "ID": key, "Question": key2, "Created_At": created}
    elif collection_name == "Score_History":
        query = {"Passcode": passcode, "Score": key, "Level": key2, "Created_At": created}
    else:
        return False, "Invalid collection name"
    collection = globals().get(collection_name)  # Get the actual collection object
    if not collection_name:
        return False, "Collection not found"
    delete_result = collection.delete_one(query)
    deleted_count = delete_result.deleted_count
    Record.insert_one(
        {
            'Passcode': this_user_passcode,
            'Action': f"User {this_user_passcode} requested to delete record {query} from {collection_name}",
            'Type': "J",
            'Created_At': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    )
    if deleted_count > 0:
        Record.insert_one(
            {
                'Passcode': this_user_passcode,
                'Action': f"Deleted 1 record for {query} from {collection_name} as requested by user {this_user_passcode}",
                'Type': "K",
                'Created_At': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        )
        return True, f"Deleted 1 record for {query} from {collection_name}"
    Record.insert_one(
        {
            'Passcode': this_user_passcode,
            'Action': f"No matching record {query} found in {collection_name} as requested by user {this_user_passcode}",
            'Type': "K",
            'Created_At': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    )
    return False, f"No matching record {query} found in {collection_name}"


# Record page side function
def sort_by_time(entry):
    return entry["Created_At"], entry["Message"]


# Record page side function
def sort_by_message(entry):
    return entry["Message"], entry["Created_At"]


# Record page side function
def sort_by_type(entry):
    return entry["Type"], entry["Created_At"], entry["Message"]


# Database page (for user) function
def create_history(passcode, priority, order, include_user, include_question, include_record,
                   include_status, include_recommendation, include_Tag,
                   include_favorite, include_removed, include_recommendation_per_person, include_question_Questionnaire,
                   include_score, this_user_passcode):
    if not User.find_one({"Passcode": passcode}):
        return False, None, "User requested not registered"
    if not User.find_one({"Passcode": this_user_passcode}):
        return False, None, "User not registered"
    query = f"Priority {priority} - Order {order} - User {include_user} - Question {include_question} - Record {include_record} - Status {include_status} - Recommendation {include_recommendation} - Tag {include_Tag} - Favorite {include_favorite} - Removed {include_removed} - Per Person {include_recommendation_per_person} - Daily Stress Questionnaire - {include_question_Questionnaire} - Score {include_score}"
    user_history = []
    message_templates = {
        "User": "User {Passcode} registered.",
        "Question": "User {Passcode} was asked '{Question}' and answered {Answer}.",
        "Record": "{Action}",
        "Status": "User {Passcode} answered Daily Stress Questionnaire.",
        "Recommendation": "User {Passcode} added recommendation '{Title}' with ID {ID}.",
        "Tag": "User {Passcode} added Tag '{Title_Of_Criteria}:{Category}' to recommendation with ID {ID}.",
        "Favorite_Recommendation": "User {Passcode} marked recommendation with ID {ID} as favorite.",
        "Removed_Recommendation": "User {Passcode} rejected recommendation with ID {ID}.",
        "Recommendation_Per_Person": "Recommendation with ID {ID} was assigned to User {Passcode} with pointer {Pointer}.",
        "Question_Questionnaire": "User {Passcode} added question '{Question}' with ID {ID}",
        "Score_History": "Score {Score} recorded for user {Passcode} at level {Level}"
    }

    # Datapage page side function
    def add_history_entries(collection_name, collection, key, key2=None):
        entries = collection.find({"Passcode": passcode})
        for entry in entries:
            new_entry = [
                {
                    'Type': collection_name,
                    'Key': entry.get(key, "N/A"),
                    'Key2': entry.get(key2, None),
                    'Message': message_templates[collection_name].format(**entry),
                    'Created_At': entry['Created_At'],
                    'Passcode': passcode
                }
            ]
            user_history.extend(new_entry)

    if include_user:
        add_history_entries("User", User, "Passcode")
    if include_question:
        add_history_entries("Question", Question, "Question")
    if include_record:
        add_history_entries("Record", Record, "Type")
    if include_status:
        add_history_entries("Status", Status, "Passcode")
    if include_recommendation:
        add_history_entries("Recommendation", Recommendation, "ID")
    if include_Tag:
        add_history_entries("Tag", Tag, "ID", "Category")
    if include_favorite:
        add_history_entries("Favorite_Recommendation", Favorite_Recommendation, "ID")
    if include_removed:
        add_history_entries("Removed_Recommendation", Removed_Recommendation, "ID")
    if include_recommendation_per_person:
        add_history_entries("Recommendation_Per_Person", Recommendation_Per_Person, "Pointer", "ID")
    if include_question_Questionnaire:
        add_history_entries("Question_Questionnaire", Question_Questionnaire, "ID", "Question")
    if include_score:
        add_history_entries("Score_History", Score_History, "Score", "Level")

    if priority == "Time":
        user_history.sort(key=sort_by_time, reverse=(order == -1))
    elif priority == "Substance":
        user_history.sort(key=sort_by_message, reverse=(order == -1))
    else:
        user_history.sort(key=sort_by_type, reverse=(order == -1))
    Record.insert_one(
        {
            'Passcode': passcode,
            'Action': f"User {this_user_passcode} requested record for {query} for user {passcode}",
            'Type': "L",
            'Created_At': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    )
    return True, user_history, f"Record for user {passcode} assembled."

