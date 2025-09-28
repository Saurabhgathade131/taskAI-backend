from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime


class TaskCreate(BaseModel):
    title: str
    description: Optional[str]
    due: Optional[datetime]
    meta: Optional[Dict[str, Any]] = {}


class TaskOut(BaseModel):
    id: str
    user_id: str
    title: str
    description: Optional[str]
    due: Optional[datetime]
    status: str
    meta: Dict[str, Any]
    created_at: datetime