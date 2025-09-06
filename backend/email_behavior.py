# backend/email_behavior.py
from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime

router = APIRouter(prefix="/behavior", tags=["behavior"])

# in-memory for now; can move to db later
user_behaviors = []

class EmailBehavior(BaseModel):
    email_id: str
    action_type: str  # "open", "hover", "click", "mark_safe", "suspend"
    timestamp: datetime = datetime.utcnow()
    duration: float = 0  # seconds for "open" action

@router.post("/")
def record_behavior(behavior: EmailBehavior):
    user_behaviors.append(behavior.dict())
    return {"message": "Behavior recorded", "total_records": len(user_behaviors)}

@router.get("/")
def get_behaviors():
    return user_behaviors
