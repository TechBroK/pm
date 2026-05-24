@echo off
REM Start PM Backend Server (Windows)
REM This script builds the frontend and starts the FastAPI backend on localhost:8000

echo Starting PM Backend Server...
echo.

REM Check if we're in the right directory
if not exist "backend\main.py" (
    echo Error: backend\main.py not found
    echo Please run this script from the project root directory
    exit /b 1
)

REM Build frontend
echo Building frontend...
cd frontend
call npm install --silent
call npm run build
cd ..

if %ERRORLEVEL% NEQ 0 (
    echo Error: Frontend build failed
    exit /b 1
)

REM Install backend dependencies if needed
echo Installing backend dependencies...
python -m pip install -q -r backend\requirements.txt

REM Start the server
echo.
echo Starting uvicorn server on http://127.0.0.1:8000
echo Press Ctrl+C to stop the server
echo.

python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload

pause
