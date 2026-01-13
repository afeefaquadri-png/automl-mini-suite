@echo off
echo Starting ML AutoML Suite Backend...
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
pause

