from os import getenv
from motor.motor_asyncio import AsyncIOMotorClient


MONGO_URI = f"mongodb://my-mongo-container:27017"
MONGO_DATABASE = getenv('MONGO_DATABASE', default='samples')

# Set up MongoDB connection pool
class Database:
    def __init__(self, client: AsyncIOMotorClient):
        self.client = client

    def get_collection(self, collection_name: str):
        return self.client[MONGO_DATABASE][collection_name]

db = Database(AsyncIOMotorClient(MONGO_URI))
