import random
from mongo_connection import Recommendation, Status, Recommendation_Per_Person
from generate_items import calculate_fail_count, get_now
from check_and_balance import get_status


# This function uses the function above to generate a valid recommendation ID, aka an ID that exists
def generate_valid_index():

    recommendation_fail = 0
    BANNED = {"Gemini", "Groq"}

    # We pick a random number between 1 and the amount of available recommendations
    # This works because the last recommendation added will have the biggest ID

    potential_recommendation_index = random.randint(1, Recommendation.count_documents({}))

    while recommendation_fail <= calculate_fail_count() and potential_recommendation_index >= 1:

        if Recommendation.find_one({"ID": potential_recommendation_index, "Passcode": {"$nin": list(BANNED)}}):

            return potential_recommendation_index  # We only return a valid not AI generated recommendation

        recommendation_fail += 1  # If the recommendation with the generated ID isn't found we add the fail count

        potential_recommendation_index = random.randint(1, Recommendation.count_documents({}))  # And we try again

    return 1


# This function gets data to add a recommendation to a user to match it with a user status
def enter_recommendation_for_user(passcode, recommendation_id, fails, category):
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
            'ID': recommendation_id,
            'Pointer': len(user_recommendations) + 1,
            'Outcome': True,
            'Fail_Count': f"{fails} / {calculate_fail_count()}",
            'Completed_At': None,
            'Status_Created_At': status['Created_At'],
            'Category': category,
            'Created_At': get_now()
        }
    )


# This Function takes a category and value from the Tag table
def pass_filter(title, category, user, status, fully_compatible=False):
    filters = [  # Create filter table with the User's information
        {'Title': 'Age Variant', 'Category': user['Age_Category']},  # From User Collection
        {'Title': 'Stress Level', 'Category': status['Stress_Level']},  # From Status Collection
        {'Title': 'Time Available', 'Category': user['Time_Available']},  # From User Collection
        {'Title': 'Show for levels above', 'Category': user['Level']},  # From User Collection
        {'Title': 'Show for levels below', 'Category': user['Level']},  # From User Collection
        {'Title': 'Show for levels equal', 'Category': user['Level']},  # From User Collection
        {'Title': 'Gender', 'Category': user['Gender']}  # From User Collection
    ]

    for focus in user.get('Focus_Area', []):
        filters.append({'Title': 'Focus Area',
                        'Category': focus})  # Users can have many focus areas, so we are splitting them in seperate lines

    condition = False

    for entry in filters:

        if entry['Title'] == title:

            condition = False

            try:
                if title == "Show for levels above":
                    # The categories with values in numbers and that need comparisons not equal need to convert the table information into numbers
                    condition = int(category) >= int(entry['Category'])
                elif title == "Show for levels below":
                    # The categories with values in numbers and that need comparisons not equal need to convert the table information into numbers
                    condition = int(category) <= int(entry['Category'])
                elif title == "Show for levels equal":
                    # The categories with values in numbers and that need comparisons not equal need to convert the table information into numbers
                    condition = int(category) == int(entry['Category'])
                elif title == "Stress Level":
                    # The categories with values in numbers and that need comparisons not equal need to convert the table information into numbers
                    condition = float(category) >= float(entry['Category'])
                elif title == "Time Available":
                    # The categories with values in numbers and that need comparisons not equal need to convert the table information into numbers
                    condition = int(category) <= int(entry['Category'])
                else:
                    condition = category == entry['Category']  # Most categories are True if the value match completely

            except (ValueError, TypeError):  # Defensive fallback: if comparison fails, treat as non-match
                condition = False

            if (condition and not fully_compatible) or (not condition and fully_compatible):
                # If fully_compatible is False then we just need one characteristic to match, if we find a positive we also abort early
                # fully_compatible means that the recommendation is appropriate is every characteristic matches the tags so abort early if one is not matching

                return condition

    # If fully_compatible was off that means condition was never True so the recommendation was never a match with the User
    # If fully_computable was on that means condition was never False so the recommendation matches the user 100%

    return condition
