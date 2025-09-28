import motor.motor_asyncio
from app.core.config import settings


class Mongo:
    def __init__(self):
        self.client = None
        self.db = None

    async def connect(self):
        self.client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGO_DSN)
        self.db = self.client[settings.MONGO_DB]
        print("✅ MongoDB connected")

    async def close(self):
        if self.client:
            self.client.close()
            print("❌ MongoDB connection closed")


# Create a single instance to reuse across the app
mongo = Mongo()
