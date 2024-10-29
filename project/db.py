import os
from pymongo import MongoClient

mongo_user = os.getenv('MONGODB_USERNAME')
mongo_password = os.getenv('MONGODB_PASSWORD')
mongo_uri = f"mongodb+srv://{mongo_user}:{mongo_password}@firstserver.z0ezt.mongodb.net/api-project?retryWrites=true&w=majority&appName=FirstServer"
client = MongoClient(mongo_uri)
db = client['api-project']
users_collection = db['users']
organizations_collection = db['organizations']