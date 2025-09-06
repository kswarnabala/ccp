# backend/gmail_api.py
from fastapi import APIRouter
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from gmail_oauth import load_gmail_token, authenticate_gmail
from ai_detector import classify_text
from storage import get_sender_state
import base64

router = APIRouter()

SAFE_THRESHOLD = 0.60  # tweakable

def get_service():
    creds = load_gmail_token()
    if not creds:
        creds = authenticate_gmail()
    return build('gmail', 'v1', credentials=creds)

def decode_part(data: str) -> str:
    if not data:
        return ""
    try:
        return base64.urlsafe_b64decode(data.encode('utf-8')).decode('utf-8', errors='ignore')
    except Exception:
        return ""

def pick_header(headers, name):
    for h in headers:
        if h.get("name") == name:
            return h.get("value", "")
    return ""

def label_to_safe_suspicious(pred):
    # pred like {"label":"LABEL_1","score":0.65}
    label = (pred.get("label") or "").upper()
    score = float(pred.get("score") or 0.0)
    is_spam_like = label in {"LABEL_1", "SPAM", "TOXIC", "NEGATIVE"}
    suspicious = is_spam_like and score >= SAFE_THRESHOLD
    return "Suspicious" if suspicious else "Safe"

@router.get("/emails")
def get_emails(max_results: int = 20, include_suspended: bool = False):
    try:
        service = get_service()
        results = service.users().messages().list(userId='me', maxResults=max_results).execute()
        messages = results.get('messages', [])
        emails = []

        for msg in messages:
            msg_data = service.users().messages().get(userId='me', id=msg['id'], format="full").execute()
            payload = msg_data.get('payload', {})
            headers = payload.get('headers', [])
            parts = payload.get('parts', [])

            sender = pick_header(headers, "From")
            subject = pick_header(headers, "Subject")

            body = ""
            if parts:
                for part in parts:
                    if part.get('mimeType') == 'text/plain':
                        body += decode_part(part.get('body', {}).get('data', ''))
            else:
                body = decode_part(payload.get('body', {}).get('data', ''))

            # AI classify (truncate done inside your ai_detector if needed)
            try:
                pred = classify_text(body or (subject or ""))
            except Exception:
                pred = {"label": "LABEL_0", "score": 0.0}

            classification = label_to_safe_suspicious(pred)

            # sender state logic
            state = get_sender_state(sender)  # "trusted" | "suspended" | None
            if state == "trusted":
                classification = "Safe"
            if state == "suspended" and not include_suspended:
                # Hide suspended senders unless explicitly asked
                continue

            emails.append({
                "id": msg['id'],
                "from": sender,
                "subject": subject,
                "snippet": msg_data.get('snippet', ''),
                "body": body,
                "classification": classification,
                "sender_state": state or "none",
            })

        return {"emails": emails}
    except HttpError as e:
        return {"emails": [], "error": str(e)}
