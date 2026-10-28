@echo off
echo ==========================================
echo Starting PlacementPilot Backend Server...
echo ==========================================
cd /d "%~dp0..\backend"
call .venv\Scripts\activate.bat
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
