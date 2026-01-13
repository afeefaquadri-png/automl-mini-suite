@echo off
echo Setting up ML AutoML Suite...
echo.


echo Creating directories...
if not exist "models" mkdir models
if not exist "data" mkdir data
if not exist "logs" mkdir logs
if not exist "reports" mkdir reports


echo.
echo Installing Python dependencies...

pip install -r requirements.txt




echo.
echo Installing Streamlit dependencies...
cd frontend_streamlit
pip install -r requirements.txt
cd ..


echo.
echo Setup complete!
echo.
echo To start the backend: run start_backend.bat
echo To start Streamlit: run start_streamlit.bat
echo To start Next.js: cd frontend_nextjs && npm install && npm run dev
pause


