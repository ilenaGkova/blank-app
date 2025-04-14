from datetime import datetime
from mongo_connection import User, Recommendation, Removed_Recommendation, Favorite_Recommendation


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

        # The new mixed table has the below fields:
        # From the Recommendations_Per_Person we keep the ID, the Pointer, the Outcome (will tell us if we will show the Done button or not)
        # The Timestamp of the status this recommendation was added to the user for, and then a statement as to how long ago the recommendation was completed
        # From the Recommendation we have the Title, Description and Points assigned (Points given will depend on the user's level)
        # The Preference is True, False or None. This indicates that the recommendation was found in the user's favorites (True), Removed (False) or has no characterisation (None)

        if not this_recommendation:  # If for any reason a recommendation that doesn't exist we need to add another right here

            Recommendation_table.append(
                {
                    'ID': entry['ID'],
                    'Pointer': entry['Pointer'],
                    'Outcome': False,
                    'Status_Created_At': entry['Status_Created_At'],
                    'Completed_At': get_time(entry['Completed_At']),
                    'Title': "Recommendation not found",
                    'Description': "We are so sorry, we can't find the recommendation",
                    'Points': 0,
                    'Preference': (
                        False if Removed_Recommendation.find_one({"ID": entry['ID'], "Passcode": passcode})
                        else True if Favorite_Recommendation.find_one({"ID": entry['ID'], "Passcode": passcode})
                        else None
                    )
                }
            )

        else:

            Recommendation_table.append(
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
            )

    return True, Recommendation_table
