@echo off
echo Checking ML AutoML Suite Services...
echo.

echo Checking Backend API (port 8000)...
curl -s http://localhost:8000/api/health >nul 2>&1
if %errorlevel% == 0 (
    echo [OK] Backend is running at http://localhost:8000
) else (
    echo [ERROR] Backend is NOT running
    echo         Start it with: start_backend.bat
)

echo.
echo Checking Streamlit Frontend (port 8501)...
curl -s http://localhost:8501 >nul 2>&1
if %errorlevel% == 0 (
    echo [OK] Streamlit is running at http://localhost:8501
) else (
    echo [ERROR] Streamlit is NOT running
    echo         Start it with: start_streamlit.bat
)

echo.
echo ========================================
echo Service Status Complete
echo ========================================
pause
