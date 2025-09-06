# backend/storage.py
import json, os, threading
DB_PATH = "sender_state.json"
_lock = threading.Lock()

def _load():
    if not os.path.exists(DB_PATH):
        return {"senders": {}}  # { email: "trusted" | "suspended" }
    with open(DB_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def _save(data):
    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def get_sender_state(sender: str) -> str | None:
    with _lock:
        return _load().get("senders", {}).get(sender)

def set_sender_state(sender: str, state: str):
    with _lock:
        data = _load()
        data.setdefault("senders", {})[sender] = state  # "trusted" | "suspended"
        _save(data)

def list_senders():
    with _lock:
        return _load().get("senders", {})
