import pymongo
import streamlit as st
from Tables import Users, Tags, Recommendations


@st.cache_resource
def init_connection():
    return pymongo.MongoClient(st.secrets["mongo"]["uri"])  # Establish Connection with database using the url given by the server in the secrets file


client = init_connection()  # Establish Connection with database using the url given by the server in the secrets file

db = client.StressTest  # Find and define the database itself

# Find the various tables in the database, you will find the name of the collection in the db["XXX"] command
# Each one will have a structured entry that will be explained later
# For now keep in mind that every entry in every collection will include a time stamp of when it was created ('Created_At') and a user passcode ('Passcode')

Status = db["Status"]  # Keeps a rating of the user's stress

User = db["User"]  # Keeps the user information for every user

Question = db["Question"]  # Keeps record for each question was given to a user and answer the user gave

Record = db[
    "Record"]  # Keeps record for actions and changes to the user information that happens once a day or a week + other requests the user has made and changes in the database done by the user

Recommendation_Per_Person = db[
    "Recommendation_Per_Person"]  # Keep a record for recommendations given to a user as paired by a status made by the user

Tag = db["Tag"]  # Will give a category of a criteria to keep users that wouldn't match a recommendation

Recommendation = db["Recommendation"]  # Will have potential recommendations to show a user

Removed_Recommendation = db[
    "Removed_Recommendation"]  # Will have a record for recommendations a user rejected to avoid giving it to them again

Favorite_Recommendation = db[
    "Favorite_Recommendation"]  # Will have a record for recommendations a user liked, so they can see them again

Question_Questionnaire = db[
    "Questionnaire"]  # Will have the questioner questions to be shown and a user can rate their stress level

Score_History = db[
    "Score_History"]  # Keeps a record for the user's score history to create a chart showing the changes of the score


# Here we have a function that will insert the default data
def insert_data():
    # Fill the database with the default data as established by the table file, with safeguards to avoid adding the twice

    if not User.find_one({"Username": "Admin"}):  # Will initialise collection User with default data

        User.insert_many(Users)

    if not Tag.find_one({"ID": 1}):  # Will initialise collection Tag with default data

        Tag.insert_many(Tags)

    if not Recommendation.find_one({"ID": 1}):  # Will initialise collection Recommendation with default data

        Recommendation.insert_many(Recommendations)
