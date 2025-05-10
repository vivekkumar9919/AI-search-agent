# db.py
from pymongo import MongoClient, errors
from dotenv import load_dotenv
import os
import sys
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

# Load environment variables
load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
DB_NAME = os.getenv("MONGO_DB_NAME", "search_agent")

try:
    client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
    # Trigger connection attempt
    client.server_info()
    db = client[DB_NAME]
    logging.info("Successfully connected to MongoDB.")
except errors.ServerSelectionTimeoutError as e:
    logging.error("Could not connect to MongoDB: %s", e)
    sys.exit(1)
except Exception as e:
    logging.error("Unexpected error while connecting to MongoDB: %s", e)
    sys.exit(1)

def get_collection(name):
    try:
        return db[name]
    except Exception as e:
        logging.error("Failed to get collection '%s': %s", name, e)
        return None
