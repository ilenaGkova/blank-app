import random
from mongo_connection import Tag, User, Status, Recommendation
from check_and_balance import get_status
from generate_recomendations_functions import enter_recommendation_for_user, generate_valid_index
from generate_items import calculate_fail_count


# This function generates a required amount of recommendations by establishing filters based on the various tags
def generate_recommendations_chosen_by_tags(passcode, entries_chosen_by_tags):
    tags = list(Tag.find())  # Gather the Tags for the recommendation to check

    user = User.find_one({"Passcode": passcode})  # Find the user using their Passcode

    # Find the last status the user made

    today, yesterday, index = get_status(passcode)

    status = Status.find_one({"_id": index})  # Use the last result to find the status to get the stress level

    filters = [
        # Establish the filters as we are watering down the recommendation we are choosing from into the ones that match the tags
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

                if Recommendation.find_one({'ID': tag['ID']}) and tag['ID'] not in user_recommendations and tag['Passcode'] != 'OpenAI':
                    recommendations.append({'ID': tag['ID'], 'Pointer': pointer})

                    user_recommendations.add(int(tag['ID']))  # Track recommendations added to avoid duplicates

                    pointer += 1

    fail_count = 0  # Set fail count to avoid loops

    index = 0  # Set counter to keep track of entries added

    user_recommendations.clear()  # Clear the user recommendations to hold the recommendations selected now

    # Handle recommendations depending on the number of results
    # If there are enough recommendations, fill the user slots by random selection and avoiding duplicates
    # Else load up all the available and fill the rest by randomly generated  from all the recommendations not just the ones appropriate

    while index < entries_chosen_by_tags:

        if len(recommendations) <= entries_chosen_by_tags:

            # Fill with available recommendations

            for entry in recommendations:
                enter_recommendation_for_user(passcode, int(entry['ID']), calculate_fail_count() + 1,
                                              'B-')  # Category B- means that while we selected a recommendation that was meant to be randomly selected by our recommendations, we had to add it in without selection

                user_recommendations.add(int(entry['ID']))  # Track recommendations added to avoid duplicates

                index += 1  # Increase to show that we added a recommendation

            # Fill remaining slots if there are not enough recommendations

            while index <= entries_chosen_by_tags:
                potential_recommendation_index = generate_valid_index()  # Generate a recommendation ID the exists

                index, fail_count, user_recommendations = validate_recommendation_pick(fail_count, index, passcode,
                                                                                       potential_recommendation_index,
                                                                                       user_recommendations,
                                                                                       'B-')  # Category B- means that while we selected a recommendation that was meant to be randomly selected by our recommendations, we had to add it in without selection

            break  # Exit the loop as we're done

        else:
            # More recommendations than needed, pick randomly without duplicates

            potential_recommendation_index = random.randint(1, pointer)

            index, fail_count, user_recommendations = validate_recommendation_pick(fail_count, index, passcode,
                                                                                   potential_recommendation_index,
                                                                                   user_recommendations, 'B')

    return index


# This function is here because the code below appeared twice in a function, it does some calculations with data and returns the new values
def validate_recommendation_pick(fail_count, index, passcode, potential_recommendation_index, user_recommendations,
                                 category):
    if potential_recommendation_index not in user_recommendations:  # User recommendation hold the recommendation already given, we can add a recommendation twice

        enter_recommendation_for_user(passcode, int(potential_recommendation_index), fail_count,
                                      category)  # Category will be B or B-. B- is explained in the bigger function, B means the recommendation was selected randomly from a list of pre-approved recommendations

        user_recommendations.add(int(potential_recommendation_index))  # Track recommendations added to avoid duplicates

        index += 1  # Increase to show that we added a recommendation

        fail_count = 0  # Keeps us from looping forever, we set it back to 0

    else:

        fail_count += 1  # Keeps us from looping forever, we increased it because we failed to find it recommendation valid to add

    if fail_count > calculate_fail_count():
        potential_recommendation_index = generate_valid_index()

        enter_recommendation_for_user(passcode, potential_recommendation_index, fail_count,
                                      'B-')  # Category B- means that while we selected a recommendation that was meant to be randomly selected by our recommendations, we had to add it in without selection

        user_recommendations.add(int(potential_recommendation_index))  # Track recommendations added to avoid duplicates

        index += 1  # Increase to show that we added a recommendation

        fail_count = 0  # Keeps us from looping forever, we set it back to 0

    return index, fail_count, user_recommendations
