from app.core.exceptions import NotFoundException, BadRequestException
from rapidfuzz import fuzz
from datetime import datetime


class TaskService:
    def __init__(self, task_repo):
        self.task_repo = task_repo

    async def create_task(self, user_id: str, data: dict):
        # validate
        if not data.get("title"):
            raise BadRequestException("title required")
        data["user_id"] = user_id
        data["created_at"] = datetime.utcnow()
        task = await self.task_repo.insert(data)
        return task

    async def list_tasks(self, user_id: str):
        return await self.task_repo.find_for_user(user_id)

    async def complete_task_by_match(self, user_id: str, text: str, candidates_limit: int = 3):
        # naive fuzzy match against user's tasks; higher-level logic belongs here
        tasks = await self.task_repo.find_for_user(user_id, limit=200)
        best = []
        for t in tasks:
            score = fuzz.token_set_ratio(text, t.get("title", ""))
            best.append((score, t))
        best.sort(key=lambda x: x[0], reverse=True)
        if not best:
            raise NotFoundException("no tasks found to match")
        top_score, top_task = best[0]
        if top_score < 60:
            # ambiguous — return candidates
            return {"ambiguous": True, "candidates": [b[1] for b in best[:candidates_limit]]}
        # apply change
        await self.task_repo.update(
            top_task["_id"], {"status": "done", "completed_at": datetime.utcnow()}
        )
        return {"ambiguous": False, "task": await self.task_repo.find_by_id(top_task["_id"])}
