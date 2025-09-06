# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from gmail_api import router as gmail_router
from logging_api import router as log_router
from email_actions import router as action_router

app = FastAPI(title="ZeroTrust-AI Mail Module")

# Allow frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "ZeroTrust-AI Mail Module Running"}

# Attach routers
app.include_router(gmail_router, prefix="/gmail")
app.include_router(log_router, prefix="/logs")
app.include_router(action_router, prefix="/actions")
