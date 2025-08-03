from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")

client = MongoClient(MONGO_URI)
db = client["qcl_datasets"]

def add_dataset(dataset: dict, name: str):
    """
    Adds dataset to MongoDB repository.
    """
    db["datasets"].insert_one({"name": name, "data": dataset})
    return {"status": "added"}
