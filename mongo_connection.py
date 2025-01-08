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

def get_database():
    return client

def insert_starter_data():
    data = get_database
    collection = data.StressUser
    for entries in Users:
        if collection.count_documents({'username': entries['username']}) == 0:
            print(f"Inserting data for user: {entries['username']}...")
            try:
                data.StressUser.insert_one(entries)
            except Exception as e:
                print(f"Error inserting data: {e}")
        else:
            print(f"Data for user: {entries['username']} already exists. Skipping insert.")
    return True
