#!/bin/bash
# Stop PM Backend Server (macOS/Linux)
# This script stops the FastAPI backend server

echo "Stopping PM Backend Server..."
echo ""

# Kill process on port 8000
if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null ; then
    echo "Terminating process on port 8000..."
    kill -9 $(lsof -t -i :8000)
    echo "Done."
else
    echo "No process found on port 8000"
fi
