from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from backend.gmail_api import get_flow, build_service_from_token, list_and_fetch_recent
from db import save_token, load_token, log_action
from ai_detector import is_suspicious_email

router = APIRouter()

REDIRECT_URI = "http://127.0.0.1:8000/auth/callback"
safe_senders = set()  # persisted in memory, can extend to DB

@router.get("/emails")
def check_emails():
    token = load_token()
    if not token:
        return JSONResponse({"error": "User not authenticated"}, status_code=401)
    
    service = build_service_from_token(token)
    emails = list_and_fetch_recent(service, max_results=10)
    out = []
    
    for e in emails:
        suspicious = is_suspicious_email(e["text"]) and e["sender"] not in safe_senders
        
        # Action required: User cannot ignore unless safe sender
        action_required = suspicious
        
        if suspicious:
            log_action({"email_id": e["id"], "sender": e["sender"], "action": "suspicious_detected"})
        
        out.append({
            "id": e["id"],
            "snippet": e["snippet"],
            "sender": e["sender"],
            "suspicious": suspicious,
            "action_required": action_required
        })
    
    return {"emails": out}

@router.post("/safe_sender/{sender_email}")
def add_safe_sender(sender_email: str):
    safe_senders.add(sender_email)
    log_action({"sender": sender_email, "action": "added_safe_sender"})
    return {"message": f"{sender_email} marked as safe"}
