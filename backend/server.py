# server.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db import init_db, get_users, save_user, update_user_status, save_log
from logging_api import router as log_router

app = FastAPI()

# Allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize DB
init_db()

# Register log routes
app.include_router(log_router)

# Fetch users
@app.get("/users")
def users():
    return {"users": [{"id": u[0], "email": u[1], "status": u[2]} for u in get_users()]}

# Add new user
@app.post("/users/add")
def add_user(email: str):
    save_user(email, "safe")
    return {"message": f"User {email} added successfully"}

# Update user status (Safe / Suspicious)
@app.post("/users/update")
def change_status(email: str, status: str):
    update_user_status(email, status)
    save_log(email, status)  # Log the action
    return {"message": f"User {email} marked as {status}"}
