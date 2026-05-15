@echo off
echo Starting AI Contract Analysis System...
echo ---------------------------------------
echo 1. Starting Backend API (Port 8000)...
start "Backend API" call uvicorn backend.main:app --reload
timeout /t 5 /nobreak
echo.
echo 2. Starting Frontend App (Port 8501)...
start "Streamlit Frontend" call streamlit run app.py
echo.
echo ==================================================
echo System is running!
echo Backend: http://localhost:8000
echo Frontend: http://localhost:8501
echo ==================================================
pause
