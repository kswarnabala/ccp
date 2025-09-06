# backend/email_actions.py
from fastapi import APIRouter
from db import set_sender_status, get_sender_status, save_log, get_suspended_senders

router = APIRouter(prefix="/actions", tags=["actions"])

@router.post("/")
def take_action(data: dict):
    sender = data.get("sender")
    action = data.get("action")

    if not sender or action not in ["safe", "suspend"]:
        return {"error": "Invalid request"}

    # update DB
    set_sender_status(sender, action)

    # log action
    save_log({"event": "action", "sender": sender, "action": action})

    return {"status": "ok", "sender": sender, "new_status": action}


@router.get("/{sender}")
def get_status(sender: str):
    return get_sender_status(sender)


@router.get("/suspended/list")
def suspended_accounts():
    """Return all suspended accounts."""
    return get_suspended_senders()
