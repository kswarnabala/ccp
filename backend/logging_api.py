# backend/logging_api.py
from fastapi import APIRouter
from db import load_logs, save_log

router = APIRouter(prefix="/logs", tags=["logs"])


@router.get("/")
def get_logs():
    """Return all logs."""
    return load_logs()


@router.post("/")
def add_log(entry: dict):
    """Add a log entry manually."""
    save_log(entry)
    return {"status": "log saved"}
