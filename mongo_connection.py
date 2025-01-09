import streamlit as st
from pymongo import MongoClient
import pymongo

# Uses st.cache_resource to only run once.
@st.cache_resource
def init_connection():
    try:
        client = pymongo.MongoClient(**st.secrets["mongo"])
        # Ping the server to check the connection
        client.admin.command('ping')
        st.success("Connected to MongoDB!")
        condition = insert_starter_data()
        return client
    except Exception as e:
        st.error(f"Error connecting to MongoDB: {e}")
        return None

client = init_connection()

# Define Starter Data
Users = [
    {'name': 'Ilena',
     'surname': 'Gkova',
     'username': 'Admin',
     'passowrd': 'Admin123',
     'repeat_preference': 5,
     'age_category': '18-25',
     'level': 1,
     'score': 500,
     'streak': 0,
     'days_summed': 0,   
     'status': 2, 
     'role': 'Admin'},
]

def insert_starter_data():
    data = init_connection()
    if data is not None:
        collection = data['StressApp']['User']
        st.sidebar.write(collection)
        for entries in Users:
            if collection.count_documents({'username': entries['username']}) == 0:
                try:
                    data['User'].insert_one(entries)
                except Exception as e:
                    print(f"Error inserting data: {e}") 
    else:
        st.error("Database connection not established. Unable to create entries.")   
    return True

def validate_user(username, password):
    query = {
        'username': username,
        'password': password
    }
    data = init_connection()
    if data is not None:
        user_collection = data['StressApp']['User']
        if user_collection.count_documents(query) == 0:
            return 1
        else:
            return 2
    else:
        st.error("Database connection not established. Please check your connection settings.")
        return 3

