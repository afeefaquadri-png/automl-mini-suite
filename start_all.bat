@echo off
echo ========================================
echo Starting ML AutoML Suite
echo ========================================
echo.

echo [1/2] Starting Backend API...
start "ML Suite Backend" cmd /k "cd backend && python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000"

timeout /t 3 /nobreak >nul

echo [2/2] Starting Streamlit Frontend...
start "ML Suite Frontend" cmd /k "cd frontend_streamlit && streamlit run app.py --server.port 8501"

echo.
echo ========================================
echo Services Started!
echo ========================================
echo.
echo Backend API: http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo.
echo Streamlit UI: http://localhost:8501
echo.
echo Press any key to open browser...
pause >nul

start http://localhost:8501

echo.
echo Both services are running in separate windows.
echo Close those windows to stop the services.
echo.
pause
