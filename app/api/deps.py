from fastapi import Depends, HTTPException, Header
from app.db.mongo import mongo
from app.repos.user_repo import UserRepo
from app.services.auth_service import AuthService
from app.core.config import settings
import jwt


async def get_db():
    return mongo.db


async def get_user_repo(db=Depends(get_db)):
    return UserRepo(db)


async def get_task_repo(db=Depends(get_db)):
    from app.repos.task_repo import TaskRepo
    return TaskRepo(db)


async def get_auth_service(user_repo=Depends(get_user_repo)):
    return AuthService(user_repo)


async def get_current_user(
    authorization: str = Header(None),
    user_repo: UserRepo = Depends(get_user_repo)
):
    """Very small example: Authorization: Bearer <token>"""
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing auth header")
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise Exception()
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
        user_id = payload.get("sub")
        user = await user_repo.find_by_id(user_id)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid authorization token")
