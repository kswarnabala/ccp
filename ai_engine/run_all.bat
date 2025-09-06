@echo off
REM ===============================
REM Setup and Run ZeroTrust-AI
REM ===============================

echo.
echo ======== 1. Create Virtual Environment for Backend ========
python -m venv venv

echo.
echo ======== 2. Activate Virtual Environment ========
call venv\Scripts\activate

echo.
echo ======== 3. Install Backend & AI Dependencies ========
pip install --upgrade pip
pip install fastapi uvicorn google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client transformers torch python-multipart requests

echo.
echo ======== 4. Start Backend Server ========
start cmd /k "call venv\Scripts\activate && cd backend && uvicorn main:app --reload"

echo.
echo ======== 5. Install Frontend Dependencies ========
cd frontend
npm install

echo.
echo ======== 6. Start Frontend Server ========
start cmd /k "cd frontend && npm start"

echo.
echo All servers started.
echo Backend: http://127.0.0.1:8000
echo Frontend: http://localhost:3000
pause
