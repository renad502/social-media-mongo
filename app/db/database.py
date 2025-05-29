from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import MONGO_URL

client: AsyncIOMotorClient = None
db = None

async def connect_to_mongo():
    global client, db
    client = AsyncIOMotorClient(MONGO_URL)
    db = client.social_media_db
    print("Connected to MongoDB")

async def close_mongo_connection():
    global client
    if client:
        client.close()
        print(" MongoDB connection closed")
