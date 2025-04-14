from datetime import datetime, timedelta
from check_and_balance import get_status
from mongo_connection import User, Recommendation_Per_Person, Status, Tag, Recommendation, Removed_Recommendation
from generate_items import calculate_fail_count, get_maximum_entries
from generate_recomendations_functions import enter_recommendation_for_user, generate_valid_index


#  This function randomly chooses a recommendation for the user based of Tags and history
def generate_recommendations_by_algorithm(passcode, entries_chosen_by_algorithm):
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
    # Find the last status the user made (look in the function for more) and make sure we enter the right amount if return variables

    today, yesterday, index = get_status(passcode)

    status = Status.find_one({"_id": index})  # Find the status to find the timestamp

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
