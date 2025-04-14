from mongo_connection import User, Recommendation_Per_Person, Question, Record, Status, Recommendation, Tag, \
    Favorite_Recommendation, Removed_Recommendation, Question_Questionnaire, Score_History
from check_and_balance import new_entry_in_record_collection


# This function gets a query and deletes an entry from a collection, easier that having seperate functions to do this!
def delete_entry(passcode, key, key2, created, collection_name, this_user_passcode):
    # Warning: There are 2 passcodes at play here. Only an admin can request to delete database data, and they can do so for every user they know the passcode of
    # So passcode -> the user whose data are requested to be deleted
    # And this_user_passcode -> the admin who makes the query

    # As always we functions called from the streamlit_app.py file we return a message and a condition that shows if the function was completed

    if not User.find_one({"Passcode": passcode}):  # Make sure the query is about a registered user
        return False, "Something went wrong, requested user not registered"

    if not User.find_one({"Passcode": this_user_passcode}):  # Make sure the query comes from a registered user
        return False, "Something went wrong, User not registered"

    # The function takes a collection name, at most 2 key identifiers of the collection if needed and the timestamp of the entry's creation
    # Depending on the collection we built a query to delete the entry
    # To see what attributes of each collection pass look for the sister function of this function create_history for more
    # Also warning, while Created_At is used in each query, we don't always need it
    # Above functions that enter data in the collections detail which entries we need to use a keys

    if collection_name == "User":
        query = {"Passcode": passcode, "Created_At": created}

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

    if not collection_name:  # End early of we couldn't have the collection object
        return False, "Collection not found"

    delete_result = collection.delete_one(query)  # Make the delete query
    deleted_count = delete_result.deleted_count  # And keep count of the result, if we did it right it will be either 0 or 1. O means the data we got were wrong somehow

    # Warning: We keep record of the delete request and the delete outcome separately
    # We also put the record under the admin who requested in, not the user whose data might have been deleted

    new_entry_in_record_collection(this_user_passcode,
                                   f"User {this_user_passcode} requested to delete record {query} from {collection_name}",
                                   "Q")

    message_for_user = f"No matching record {query} found in {collection_name} as requested by user {this_user_passcode}"

    if deleted_count > 0:
        message_for_user = f"Deleted 1 record for {query} from {collection_name} as requested by user {this_user_passcode}"

    new_entry_in_record_collection(this_user_passcode, message_for_user, "Q")

    return deleted_count > 0, message_for_user


# This function gets an entry that was created in add_history_entries and returns the TimeStamp of creation and content
def sort_by_time(entry):
    return entry["Created_At"], entry[
        "Message"]  # The result of all the entries will be sorted by creation time and then content


# This function gets an entry that was created in add_history_entries and returns the TimeStamp of creation and content
def sort_by_message(entry):
    return entry["Message"], entry[
        "Created_At"]  # The result of all the entries will be sorted by content and then creation time


# This function gets an entry that was created in add_history_entries and returns the TimeStamp of creation, content and Type aka collection name
def sort_by_type(entry):  # Find_me
    return entry["Type"], entry["Created_At"], entry[
        "Message"]  # The result will be grouped by collection name, then by creation time then content. It's the default sorting method if one isn't specified


# This function gets data about a collection, including the collection itself and populates the table given with entries before returning it
def add_history_entries(passcode, user_history, collection_name, collection, key, key2=None):
    # Each collection is built differently. All have a passcode attribute and a Created_At timestamp but all have different uses and other data stored in
    # Our goal is to condense that data into a message that shows the collection entry

    message_templates = {
        # This table refers to attributes in the collection it's about by name, not value. We have one for each collection
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

    entries = collection.find({
                                  "Passcode": passcode})  # We have to global variable for the collection, so we use it to only get the data for the user

    for entry in entries:  # For each entry we have

        user_history.append(
            {
                'Type': collection_name,  # The collection it came from
                'Key': entry.get(key, "N/A"),
                # 1 to 2 key attributes for the entry in the collection, so we can delete this entry on command later
                'Key2': entry.get(key2, None),
                'Message': message_templates[collection_name].format(**entry),  # A message as dictated above
                'Created_At': entry['Created_At'],
                # The timestamp of the general creation for the entry in the collection - not the current time
                'Passcode': passcode  # The user passcode
            }
        )

    return user_history


# This function get data to make a record of the user's footprint in the database
def create_history(passcode, priority, order, include_user, include_question, include_record,
                   include_status, include_recommendation, include_Tag,
                   include_favorite, include_removed, include_recommendation_per_person, include_question_Questionnaire,
                   include_score, this_user_passcode):
    # Warning: There are 2 passcodes at play here. All users can look up their own history but an Admin can look for another user
    # So passcode -> the user whose data are requested to be found
    # And this_user_passcode -> the admin who makes the query

    # The function returns 3 things back: an indicator if the function was completed, a dictionary table and a message

    if not User.find_one({"Passcode": passcode}):  # Make sure the query is about a registered user
        return False, None, "Something went wrong, requested user not registered"

    if not User.find_one({"Passcode": this_user_passcode}):  # Make sure the query comes from a registered user
        return False, None, "Something went wrong, User not registered"

    user_history = []  # Initialise the table we will return

    # We have in total 10 collections in the database. The function receives 10 boolean variables the dectate whether a collection will be added in the record or not
    # We enrich the table user_history depending on the True/False value of the variable
    # We use the above function add_history_entries to create the entries, look for the structure of the table in the function
    # We sent to that function the passcode of the user, the table to add the entries in and most important 1 key attribute name for the collection
    # Some collections require more than passcode and one key attribute so some will also send key2 as the second name of an attribute
    # Warning: We do not sent the value of the key attributes, but their names
    # We also send the variable that holds the collection here, the global ones that got connected with the database

    if include_user:
        user_history = add_history_entries(passcode, user_history, 'User', User, "Passcode")

    if include_question:
        user_history = add_history_entries(passcode, user_history, "Question", Question, "Question")

    if include_record:
        user_history = add_history_entries(passcode, user_history, "Record", Record, "Type")

    if include_status:
        user_history = add_history_entries(passcode, user_history, "Status", Status, "Passcode")

    if include_recommendation:
        user_history = add_history_entries(passcode, user_history, "Recommendation", Recommendation, "ID")

    if include_Tag:
        user_history = add_history_entries(passcode, user_history, "Tag", Tag, "ID", "Category")

    if include_favorite:
        user_history = add_history_entries(passcode, user_history, "Favorite_Recommendation", Favorite_Recommendation,
                                           "ID")

    if include_removed:
        user_history = add_history_entries(passcode, user_history, "Removed_Recommendation", Removed_Recommendation,
                                           "ID")

    if include_recommendation_per_person:
        user_history = add_history_entries(passcode, user_history, "Recommendation_Per_Person",
                                           Recommendation_Per_Person, "Pointer", "ID")

    if include_question_Questionnaire:
        user_history = add_history_entries(passcode, user_history, "Question_Questionnaire", Question_Questionnaire,
                                           "ID", "Question")

    if include_score:
        user_history = add_history_entries(passcode, user_history, "Score_History", Score_History, "Score", "Level")

    # The table has been populated, so now we look for the sorting method the user picked in the priority
    # Look for the functions sort_by_time, sort_by_message, sort_by_type to understand how each method works

    if priority == "Time":
        user_history.sort(key=sort_by_time, reverse=(order == -1))

    elif priority == "Substance":  # Substance means content, look at how we populate this table to understand
        user_history.sort(key=sort_by_message, reverse=(order == -1))

    else:
        user_history.sort(key=sort_by_type, reverse=(order == -1))

    # Describe the query to log the search into the user's record - that is the user who requested this query who might not be the user whom this record is about

    query = f"Priority {priority} - Order {order} - User {include_user} - Question {include_question} - Record {include_record} - Status {include_status} - Recommendation {include_recommendation} - Tag {include_Tag} - Favorite {include_favorite} - Removed {include_removed} - Per Person {include_recommendation_per_person} - Daily Stress Questionnaire - {include_question_Questionnaire} - Score {include_score}"

    new_entry_in_record_collection(this_user_passcode,
                                   f"User {this_user_passcode} requested record for {query} for user {passcode}", "Q")

    return True, user_history, f"Record for user {passcode} assembled."



