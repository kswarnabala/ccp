# api_routes.py
from fastapi import APIRouter
from backend.gmail_api import build_service_from_token, list_and_fetch_recent
from backend.ai_detector import is_phishing_email
from db import load_token, log_action

router = APIRouter()

@router.get("/emails/recent")
def get_recent_emails():
    token = load_token()
    if not token:
        return {"error": "User not authenticated"}
    
    service = build_service_from_token(token)
    emails = list_and_fetch_recent(service, max_results=10)
    
    for e in emails:
        phishing = is_phishing_email(e["snippet"], e["text"])
        e["is_phishing"] = phishing
        
        # Log detection
        log_action({
            "email_id": e["id"],
            "phishing_detected": phishing
        })
    return emails

@router.post("/emails/action")
def take_email_action(email_id: str, suspend: bool):
    """
    Record user decision on suspicious email.
    If suspend=True, account flagged; if False, log decision but cannot mark as safe.
    """
    log_action({
        "email_id": email_id,
        "user_suspend_choice": suspend
    })
    return {"message": "Action recorded"}
