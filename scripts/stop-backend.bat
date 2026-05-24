@echo off
REM Stop PM Backend Server (Windows)
REM This script stops the FastAPI backend server

echo Stopping PM Backend Server...
echo.

REM Kill process on port 8000
for /f "tokens=5" %%a in ('netstat -ano ^| find ":8000"') do (
    echo Terminating process %%a on port 8000...
    taskkill /PID %%a /F
)

echo Done.
pause
