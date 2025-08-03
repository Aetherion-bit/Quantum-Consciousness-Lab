from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")

client = MongoClient(MONGO_URI)
db = client["consciousness_lab"]

def insert_session(data: dict):
    """
    Inserts a session into MongoDB.
    """
    return db["sessions"].insert_one(data).inserted_id
