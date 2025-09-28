from abc import ABC, abstractmethod


class BaseRepo(ABC):
    def __init__(self, db):
        self._db = db

    @abstractmethod
    async def insert(self, obj):
        raise NotImplementedError

    @abstractmethod
    async def find_one(self, *args, **kwargs):
        raise NotImplementedError
