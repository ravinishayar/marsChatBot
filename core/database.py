import os
from pymongo import MongoClient
from dotenv import load_dotenv

# 🔐 Load .env environment variables
load_dotenv()

# ✅ Get Mongo URI from environment variable
MONGO_URI = os.getenv("MONGO_DB_URI")

if not MONGO_URI:
    raise ValueError("⚠️ MONGO_DB_URI environment variable is not set!")

# 🔗 Connect to MongoDB
client = MongoClient(MONGO_URI)

# 📂 Select your database and collection
db = client["radhekrishn456"]  # ✅ Your database name
user_collection = db["users"]  # ✅ Your collection name


# 🔁 Return users collection
def get_user_collection():
    return user_collection
