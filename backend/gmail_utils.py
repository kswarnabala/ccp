# gmail_utils.py
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from gmail_oauth import load_gmail_token, authenticate_gmail
from ai_detector import classify_text
from email_actions import get_sender_status
import base64
import html
import re

def _get_plain_text_from_parts(parts):
    text = ""
    for part in parts:
        mime = part.get("mimeType", "")
        if mime == "text/plain":
            data = part.get("body", {}).get("data")
            if data:
                text += base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore")
        elif mime == "text/html":
            data = part.get("body", {}).get("data")
            if data:
                raw = base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore")
                # crude html -> text
                cleaned = re.sub(r"<script.*?>.*?</script>", "", raw, flags=re.DOTALL|re.IGNORECASE)
                cleaned = re.sub(r"<style.*?>.*?</style>", "", cleaned, flags=re.DOTALL|re.IGNORECASE)
                cleaned = re.sub(r"<[^>]+>", "", cleaned)
                cleaned = html.unescape(cleaned)
                text += cleaned
        # nested parts
        if part.get("parts"):
            text += _get_plain_text_from_parts(part.get("parts"))
    return text

def extract_text_from_message(msg):
    payload = msg.get("payload", {})
    if payload.get("parts"):
        return _get_plain_text_from_parts(payload["parts"]).strip()
    else:
        data = payload.get("body", {}).get("data")
        if data:
            return base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore").strip()
    return ""

def fetch_all_emails(max_results=100):
    """
    Fetch emails and classify them. Returns list of emails with classification.
    max_results is the limit for messages.list (Gmail caps) - use pagination in production.
    """
    creds = load_gmail_token()
    if not creds:
        # trigger browser auth (synchronous)
        authenticate_gmail(start_browser=True)
        creds = load_gmail_token()
        if not creds:
            raise RuntimeError("Authentication failed or cancelled.")

    service = build("gmail", "v1", credentials=creds)
    try:
        resp = service.users().messages().list(userId="me", maxResults=max_results).execute()
        messages = resp.get("messages", [])
        out = []
        for m in messages:
            msg_data = service.users().messages().get(userId="me", id=m["id"], format="full").execute()
            snippet = msg_data.get("snippet", "")
            headers = msg_data.get("payload", {}).get("headers", [])
            subject = next((h["value"] for h in headers if h["name"].lower() == "subject"), "")
            from_header = next((h["value"] for h in headers if h["name"].lower() == "from"), "")
            sender = from_header

            body = extract_text_from_message(msg_data)
            # classification: truncate to avoid huge sequences
            short_body = (body[:4000] + "...") if len(body) > 4000 else body

            # If sender suspended -> mark suspended
            status = get_sender_status(sender)
            if status == "suspended":
                classification = {"label": "SUSPENDED", "score": 1.0}
            else:
                classification = classify_text(short_body)

            out.append({
                "id": m["id"],
                "from": sender,
                "subject": subject,
                "snippet": snippet,
                "body": body,
                "classification": classification
            })
        return out
    except HttpError as e:
        raise RuntimeError(f"Gmail API error: {e}")
