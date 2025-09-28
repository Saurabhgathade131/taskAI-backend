from fastapi import APIRouter, Depends, HTTPException
from app.api.deps import get_task_repo, get_current_user
from app.services.task_service import TaskService
from app.schemas.task import TaskCreate

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/")
async def create_task(
    payload: TaskCreate,
    current_user=Depends(get_current_user),
    task_repo=Depends(get_task_repo)
):
    svc = TaskService(task_repo)
    created = await svc.create_task(str(current_user.get("_id")), payload.dict())
    return {"task": created}


@router.get("/")
async def list_tasks(
    current_user=Depends(get_current_user),
    task_repo=Depends(get_task_repo)
):
    svc = TaskService(task_repo)
    return {"tasks": await svc.list_tasks(str(current_user.get("_id")))}


@router.post("/complete_by_text")
async def complete_by_text(
    body: dict,
    current_user=Depends(get_current_user),
    task_repo=Depends(get_task_repo)
):
    text = body.get("text")
    if not text:
        raise HTTPException(status_code=400, detail="text required")
    svc = TaskService(task_repo)
    return await svc.complete_task_by_match(str(current_user.get("_id")), text)
