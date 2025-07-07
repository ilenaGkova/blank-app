from datetime import datetime
from mongo_connection import Status, User, Record, Score_History, Question
from generate_items import get_limits, get_now


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
                'Created_At': get_now()
            }
        )

        return True, "Status recorded"


# Here we have the function that inserts an entry in a record collection
def new_entry_in_record_collection(passcode, action, letter):
    # Each entry has 3 attributes that combined will identify the entry in the collection: Passcode, Type and Created_At
    # While Passcode and Type are used usually to track whether an action has already been done, so it isn't done twice
    # Type is a letter assigned to the type of action. While Action is more detailed Type is a letter:

    # Type C is data for the user's commitment to the application
    # That includes changes in the days they have been connected, continuous days connected and completing recommendations

    # Type P is for profile data, look here for profile creations, log ins and profile updates

    # Type Q is for query in database, look here for queries to gather record data and delete entries

    # Type S is for Score. Includes changes in the level or score of a user

    Record.insert_one(
        {
            'Passcode': passcode,  # The user passcode to find the user if needed
            'Action': action,  # Describing the action done in words
            'Type': letter,
            'Created_At': get_now()
        }
    )


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
            'Created_At': get_now()
        }
    )


# This function records a question and an answer the user has given
def record_question(question, answer, passcode, function=True):
    # The function has 2 returns
    # One is a message of the outcome of the function and the other is True/False
    # True means the function completed its task: recording the question/answer

    # The last parameter 'function' is rarely given and is here because 1, only 1, action in the application will have an additional filter to make sure the question needs to be recorded
    # It's a disclaimer and there isn't a middle function to weed out the unfit entries
    # Usually the function will be called when the data have already been verified

    answer = str(answer)

    if not answer.strip() or not question.strip() or not function:
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
            'Created_At': get_now()
        }
    )

    return True, "Question recorded"
