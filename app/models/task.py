from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class TaskInDB(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    user_id: str
    title: str
    description: Optional[str] = None
    due: Optional[datetime] = None
    status: str = "pending"
    meta: dict = {}
    timestamps: dict = {}
    duration_seconds: int = 0
    source: str = "chat"
    created_at: datetime = datetime.utcnow()
