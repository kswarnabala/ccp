# backend/db.py

# In-memory database (replace with MongoDB/Postgres later if needed)

# --- Email senders database ---
senders_db = {}  # { "sender@email.com": {"status": "safe" or "suspend"} }

# --- Logs database ---
logs = []


# -------------------------------
# Senders
# -------------------------------
def set_sender_status(sender: str, status: str):
    """Set the status (safe/suspend) for a sender."""
    senders_db[sender] = {"status": status}


def get_sender_status(sender: str):
    """Return the status of a sender."""
    return senders_db.get(sender, {"status": "unknown"})


def get_all_senders():
    """Return all senders and their statuses."""
    return senders_db


def get_suspended_senders():
    """Return only suspended senders."""
    return {s: info for s, info in senders_db.items() if info["status"] == "suspend"}


# -------------------------------
# Logs
# -------------------------------
def save_log(entry: dict):
    """Save a log entry."""
    logs.append(entry)


def load_logs():
    """Get all saved logs."""
    return logs
