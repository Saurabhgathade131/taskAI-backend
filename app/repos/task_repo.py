from app.repos.base_repo import BaseRepo
from bson import ObjectId


class TaskRepo(BaseRepo):
    COLLECTION = "tasks"

    async def insert(self, task_dict: dict):
        res = await self._db[self.COLLECTION].insert_one(task_dict)
        task_dict["_id"] = str(res.inserted_id)
        return task_dict

    async def find_by_id(self, id_: str):
        row = await self._db[self.COLLECTION].find_one({"_id": ObjectId(id_)})
        return row

    async def find_for_user(self, user_id: str, limit: int = 50):
        cursor = self._db[self.COLLECTION].find({"user_id": user_id}).sort("created_at", -1).limit(limit)
        return [r async for r in cursor]

    async def update(self, id_: str, update: dict):
        await self._db[self.COLLECTION].update_one({"_id": ObjectId(id_)}, {"$set": update})
        return await self.find_by_id(id_)
