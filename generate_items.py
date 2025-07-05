import string
import random
from mongo_connection import User, db, Recommendation, Recommendation_Per_Person, Tag, Favorite_Recommendation, \
    Removed_Recommendation


# This function generates a unique passcode, a 10-digit number that isn't in any collection to make sure no confusions happen
def generate_unique_passcode(length=8):
    attempt_count = 0

    # Bellow is the names of collections in the database in a table

    all_collections = [
        "Status", "User", "Question", "Record", "Recommendations_Per_Person",
        "Tag", "Recommendation", "Removed_Recommendation", "Favorite_Recommendation"
    ]

    while attempt_count < 100:

        characters = string.ascii_letters + string.digits

        passcode = ''.join(random.choices(characters, k=length))

        passcode_exists = False

        for collection_name in all_collections:  # Go through all the collections to find the number

            collection = db[collection_name]  # Get the collection using the table above to get the name

            if collection.find_one({"Passcode": passcode}):
                passcode_exists = True

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


# This function generates a recommendation ID for a new recommendation to be added
def generate_recommendation_id():
    last_entry = Recommendation.find_one(sort=[("ID", -1)])  # Step 1: Get the biggest ID in recommendation collection

    if last_entry:  # Step 2: Increase the biggest ID by one if there are recommendations, or set the new ID as 1

        generated_id = int(last_entry['ID']) + 1

    else:

        generated_id = 1

    while Recommendation.find_one({"ID": generated_id}) or Tag.find_one({"ID": generated_id}) or Recommendation_Per_Person.find_one({"ID": generated_id}) or Favorite_Recommendation.find_one({"ID": generated_id}) or Removed_Recommendation.find_one({"ID": generated_id}):
        generated_id += 1  # Step 3: Increase by 1 until the new id doesn't exist

    return generated_id


# This Function returns 2 things. The minimum limit for the recommendations a user can request when ending their information and the additional they can request via a button
def get_maximum_entries():
    return min(int(Recommendation.count_documents({"Passcode": {"$nin": ["Gemini", "Groq"]}}) / 10), 5), min(int(Recommendation.count_documents({"Passcode": {"$nin": ["Gemini", "Groq"]}}) * 0.1), 3)


# This function gets a level and will calculate the limit score of the level.
def get_limits(level):
    # The calculations below calculate the promotion score. In sum, it's level^2 * 100

    x = 100 * level
    move_up_threshold = x*level

    # The calculations below calculate the demotion score. It relies on the promotion score and the level

    y = max(0, 50 - 5 * level)  # Prevents negative or too small y
    move_down_threshold = move_up_threshold * (1 - y / 100)
    move_down_threshold = min(move_down_threshold,
                              move_up_threshold * 0.95)  # Ensure demotion threshold is at most 95% of the promotion threshold
    if level == 1:
        return move_up_threshold, 0

    if level == 25:
        return 10**9, move_down_threshold
    return move_up_threshold, move_down_threshold


# This function calculates the amount of times an algorithm can fail to find an appropriate recommendation for a user depending on the amount of recommendations available
def calculate_fail_count():
    number_of_recommendations_in_total = Recommendation.count_documents({"Passcode": {"$nin": ["Gemini", "Groq"]}})  # Step 1: Get the current number of recommendations in the Database

    total_possible_IDs = Recommendation.find_one({"Passcode": {"$nin": ["Gemini", "Groq"]}}, sort=[('ID', -1)])[
        'ID']  # Step 2: Get the ID of the last entered recommendation

    number_of_recommendation_after_removing_deleted_entries = total_possible_IDs - number_of_recommendations_in_total  # Step 3: Find the actual amount of recommendations by subtracting the biggest ID with the number of recommendations

    # The recommendations come with IDs from 1 and up
    # With deleted entries the IDs might go 1, 2, 4, 5
    # When a new recommendation is added the ID is set at the amount or recommendations + 1

    # Step 4: Return the appropriate amount of fails based of all of the above
    # We add 2 because when there are not deleted entries in the answer is 1, and we want to add some margin of error

    return (int(total_possible_IDs / (
            max(number_of_recommendations_in_total - number_of_recommendation_after_removing_deleted_entries, 2)))) + 2
