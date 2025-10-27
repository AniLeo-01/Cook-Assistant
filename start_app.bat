@echo off
REM Cook Assistant Startup Script for Windows

echo.
echo Starting Cook Assistant Application...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed. Please install Python 3.10 or higher.
    pause
    exit /b 1
)

REM Check and install dependencies
echo Checking dependencies...
python -c "import fastapi" 2>nul
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
)

echo.
echo Dependencies OK
echo.

REM Start backend
echo Starting backend server...
start "Cook Assistant Backend" python run_backend.py

REM Wait for backend to start
timeout /t 3 /nobreak >nul

REM Start UI
echo Starting UI server...
start "Cook Assistant UI" python run_ui.py

echo.
echo ============================================
echo Cook Assistant is running!
echo ============================================
echo.
echo Backend API: http://localhost:8080
echo Streamlit UI: http://localhost:8501
echo.
echo Close the command windows to stop the servers
echo.

pause

