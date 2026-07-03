from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://healthlens:<db_password>@cluster0.1pxbmpd.mongodb.net/?appName=Cluster0")

client = None
db = None

def connect_db():
    global client, db
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        db = client["healthlens_db"]
        print("Connected to MongoDB Atlas")
    except Exception as e:
        print(f"Database connection warning: {e}")

def get_db():
    if db is None:
        connect_db()
    return db
