from datetime import datetime
import random
from mongo_connection import Recommendation, Status, Recommendation_Per_Person
from generate_items import calculate_fail_count
from check_and_balance import get_status


# This function uses the function above to generate a valid recommendation ID, aka an ID that exists
def generate_valid_index():
    recommendation_fail = 0

    # We pick a random number between 1 and the amount of available recommendations
    # This works because the last recommendation added will have the biggest ID

    potential_recommendation_index = random.randint(1, Recommendation.count_documents({}))

    while recommendation_fail <= calculate_fail_count() and potential_recommendation_index >= 1:

        if Recommendation.find_one({"ID": potential_recommendation_index}):

            if Recommendation.find_one({"ID": potential_recommendation_index})["Passcode"] != "OpenAI":

                return potential_recommendation_index  # We only return a valid not AI generated recommendation

        recommendation_fail += 1  # If the recommendation with the generated ID isn't found we add the fail count

        potential_recommendation_index = random.randint(1, Recommendation.count_documents({}))  # And we try again

    if recommendation_fail > calculate_fail_count():  # We use the above function to stop the algorithm form going in a look

        potential_recommendation_index = Recommendation.find_one({"Passcode": {"$ne": "OpenAI"}}, sort=[('ID', -1)])['ID']  # In this case we pick the first available ID in the collection

        if potential_recommendation_index is None:

            return Recommendation.find_one({"Passcode": {"$ne": "OpenAI"}}, sort=[('ID', -1)])['ID']  # In this case we pick the first available ID in the collection

    return potential_recommendation_index


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

def pass_filter(title, category, user, status, out_early=False):

    filters = [
        # Establish the filters as we are watering down the recommendation we are choosing from into the ones that match the tags
        {'Title_Of_Criteria': 'Age Variant', 'Category': user['Age_Category']},
        {'Title_Of_Criteria': 'Stress Level', 'Category': status['Stress_Level']},
        {'Title_Of_Criteria': 'Time Available', 'Category': user['Time_Available']},
        {'Title_Of_Criteria': 'Show for levels above', 'Category': user['Level']},
        {'Title_Of_Criteria': 'Show for levels below', 'Category': user['Level']},
        {'Title_Of_Criteria': 'Show for levels equal', 'Category': user['Level']},
    ]

    for entry in user['Focus_Area']:
        filters.append({'Title_Of_Criteria': 'Focus Area', 'Category': entry})

    for entry in filters:

        if title == entry['Title_Of_Criteria']:

            condition = True

            if title == "Time Available" or title == "Show for levels below":

                if int(category) > int(entry['Category']):

                    condition = False

            elif title == "Show for levels above":

                if int(category) < int(entry['Category']):

                    condition = False

            elif title == "Show for levels equal":

                if category != entry['Category']:

                    condition = False

            elif category != entry['Category']:

                condition = False

            if (out_early and not condition) or (not out_early and condition):
                return condition

    return condition
