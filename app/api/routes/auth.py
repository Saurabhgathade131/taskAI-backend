from fastapi import APIRouter, Depends, HTTPException
from app.api.deps import get_user_repo, get_auth_service
from app.schemas.user import UserCreate
from app.core.exceptions import ConflictException

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register")
async def register(
    payload: UserCreate,
    user_repo=Depends(get_user_repo),
    auth_service=Depends(get_auth_service),
):
    existing = await user_repo.find_by_email(payload.email)
    if existing:
        raise ConflictException("Email already registered")

    hashed = auth_service.hash_password(payload.password)
    user = {
        "name": payload.name,
        "email": payload.email,
        "password_hash": hashed,
        "settings": {},
    }
    created = await user_repo.insert(user)
    token = auth_service.create_access_token(str(created.get("_id")))

    return {
        "token": token,
        "user": {
            "id": created.get("_id"),
            "name": created.get("name"),
            "email": created.get("email"),
        },
    }


@router.post("/login")
async def login(
    payload: UserCreate,
    user_repo=Depends(get_user_repo),
    auth_service=Depends(get_auth_service),
):
    user = await user_repo.find_by_email(payload.email)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not auth_service.verify(payload.password, user.get("password_hash")):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = auth_service.create_access_token(str(user.get("_id")))

    return {
        "token": token,
        "user": {
            "id": user.get("_id"),
            "name": user.get("name"),
            "email": user.get("email"),
        },
    }
