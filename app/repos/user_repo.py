from app.repos.base_repo import BaseRepo
from bson import ObjectId

class UserRepo(BaseRepo):
    COLLECTION = "users"

    async def insert(self, user_dict: dict):
        res = await self._db[self.COLLECTION].insert_one(user_dict)
        user_dict["_id"] = str(res.inserted_id)
        return user_dict

    async def find_by_email(self, email: str):
        return await self._db[self.COLLECTION].find_one({"email": email})

    async def find_by_id(self, id_: str):
        return await self._db[self.COLLECTION].find_one({"_id": ObjectId(id_)})

    async def find_one(self, query: dict):
        return await self._db[self.COLLECTION].find_one(query)
