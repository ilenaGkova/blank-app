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

            if Recommendation.find_one({"ID": potential_recommendation_index})["Passcode"] != "Gemini" or Recommendation.find_one({"ID": potential_recommendation_index})["Passcode"] != "Groq":

                return potential_recommendation_index  # We only return a valid not AI generated recommendation

        recommendation_fail += 1  # If the recommendation with the generated ID isn't found we add the fail count

        potential_recommendation_index = random.randint(1, Recommendation.count_documents({}))  # And we try again

    if recommendation_fail > calculate_fail_count():  # We use the above function to stop the algorithm from going in a loop

        potential_recommendation_index = Recommendation.find_one(
            {"Passcode": {"$nin": ["Gemini", "Groq"]}},
            sort=[("ID", -1)],
            projection={"ID": 1, "_id": 0}
        )
        if potential_recommendation_index is None:
            return 1

    return potential_recommendation_index["ID"]


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
        {'Title': 'Age Variant', 'Category': user['Age_Category']},
        {'Title': 'Stress Level', 'Category': status['Stress_Level']},
        {'Title': 'Time Available', 'Category': user['Time_Available']},
        {'Title': 'Show for levels above', 'Category': user['Level']},
        {'Title': 'Show for levels below', 'Category': user['Level']},
        {'Title': 'Show for levels equal', 'Category': user['Level']},
        {'Title': 'Gender', 'Category': user['Gender']}
    ]

    for focus in user.get('Focus_Area', []):
        filters.append({'Title': 'Focus Area', 'Category': focus})

    for entry in filters:
        if entry['Title'] != title:
            continue  # Only care about filters that match the title

        user_val = entry['Category']

        if title == "Show for levels above":
            condition = int(category) >= int(user_val)
        elif title == "Show for levels below":
            condition = int(category) <= int(user_val)
        elif title == "Show for levels equal":
            condition = int(category) == int(user_val)
        elif title == "Stress Level":
            condition = float(category) >= float(user_val)
        elif title == "Time Available":
            condition = int(category) <= int(user_val)
        else:
            condition = category == user_val

        if out_early:
            if not condition:
                return False  # One failure = reject immediately
        else:
            if condition:
                return True  # One match = accept immediately

    # After looping all filters
    if out_early:
        return True  # Passed all matches without failing
    else:
        return False  # No matches found


