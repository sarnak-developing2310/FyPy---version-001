from pymongo import MongoClient

# Use your provided MongoDB connection string
MONGO_URI = "mongodb+srv://mallicksarnak:GUez6UlelI3QON2t@diversion2k25.kv6vi.mongodb.net/"

# Connect to MongoDB
client = MongoClient(MONGO_URI)

# Select your database – change "financehub" to your desired DB name if needed.
db = client["financehub"]

# Example: Get a collection reference (e.g., "users")
users_collection = db["users"]

def get_users():
    """Return a list of user documents from the 'users' collection."""
    return list(users_collection.find())

def add_user(user_data):
    """
    Insert a new user document into the 'users' collection.
    user_data should be a dictionary with user information.
    Returns the result of the insertion.
    """
    return users_collection.insert_one(user_data)