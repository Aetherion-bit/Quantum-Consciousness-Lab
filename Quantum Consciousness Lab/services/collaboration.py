from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")

client = MongoClient(MONGO_URI)
db = client["consciousness_lab"]

def create_collaboration_session(user_id: str, data: dict):
    """
    Creates a shared session for collaborative analysis.
    """
    session_id = db["collaborations"].insert_one({"user_id": user_id, "data": data}).inserted_id
    return {"session_id": str(session_id)}
