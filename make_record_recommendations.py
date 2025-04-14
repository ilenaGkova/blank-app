from mongo_connection import Recommendation, Removed_Recommendation, Favorite_Recommendation, Recommendation_Per_Person, \
    User
from check_and_balance import new_entry_in_record_collection


# This function will build an entry for a table around a recommendation ID
def create_entry(index, passcode, collection, outcome, created):
    this_recommendation = Recommendation.find_one(
        {"ID": index})  # Find the recommendation to get other information on it

    if this_recommendation:  # We will create an entry regardless if we find the recommendation

        # We include the Title / Description / ID from the recommendation
        # We include the ID / Collection Name / Outcome and the TimeStamp  for the creation of the entry in the collection as given to the function
        # We have a boolean attribute the shows we can extend this recommendation to see it in full, basically that it exists currently
        # If the recommendation is in either the favorites / removed category we add that we can remove it from them
        # The last 2 dictate if a button will appear next to this entry

        return [
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

        # If we can't find the recommendation we default everything to avoid errors popping up

        return [
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


# This function dictates whether a recommendation found in a collection needs to be added to a table, it returns a made table ot None
def add_collection(passcode, status, collection_name, collection, completed):
    if not status:  # Status refers to whether or not we want to add the collection to the table
        return None

    data_table = []  # Initialise the table we will return later

    data = collection.find({"Passcode": passcode})  # Our data is the recommendations under the user's passcode

    for entry in data:

        outcome = None  # Default outcome as None, we only change it if it exists in the collection

        if collection == Recommendation_Per_Person:  # Only one connection will be having an outcome we need to match with the requested outcome, completed
            outcome = entry['Outcome']

        if (collection == Recommendation_Per_Person and (
                outcome == completed or completed is None)) or collection != Recommendation_Per_Person:
            data_table.extend(create_entry(entry['ID'], passcode, collection_name, outcome, entry[
                'Created_At']))  # See function above to see how we create an entry at the table we return

    return data_table


# This function gets an entry that was created in create_entry and returns the TimeStamp of creation and ID number
def sort_by_created_by(entry):
    return entry["Created_At"], entry["ID"]


#  This function gets a request from a user about their application history data around the recommendations and makes a record
def create_recommendation_history(passcode, order, include_favorite, include_removed,
                                  include_Recommendations, completed):
    # Along with the data we return a message for the user and in indication if the function completed the requested function

    user = User.find_one({"Passcode": passcode})  # Find the user using their Passcode

    query = f"Order: {order} - Favorite {include_favorite} - Removed {include_removed} - Per Person {include_Recommendations} / {completed}"  # Describe the query so the record can be made

    if not user:  # End early if user not found
        return False, None, "Something went wrong, user not registered"

    user_recommendation = []  # Initialise table

    # We have 3 collections to run through, for each we will call the function the constructs a temporary table, and we will add it to ours if it's not None. None means the use doesn't want to see it
    # The collection will be found as the collection_name or the 3 variable in the variables given to the add_collection function

    temporary_table = add_collection(passcode, include_favorite, "Favorite_Recommendation", Favorite_Recommendation,
                                     None)
    if temporary_table is not None:
        user_recommendation.extend(temporary_table)

    temporary_table = add_collection(passcode, include_removed, "Removed_Recommendation", Removed_Recommendation, None)

    if temporary_table is not None:
        user_recommendation.extend(temporary_table)

    temporary_table = add_collection(passcode, include_Recommendations, "Recommendation_Per_Person",
                                     Recommendation_Per_Person,
                                     completed)  # Completed refers to the recommendations per person collection

    if temporary_table is not None:
        user_recommendation.extend(temporary_table)

    user_recommendation.sort(key=sort_by_created_by,
                             reverse=(order == -1))  # Arrange the data timestamp first and then ID

    new_entry_in_record_collection(passcode,
                                   f"User {passcode} requested recommendation record for {query}",
                                   "Q")

    return True, user_recommendation, f"Record for user {passcode} assembled."
