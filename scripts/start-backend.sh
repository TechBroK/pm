#!/bin/bash
# Start PM Backend Server (macOS/Linux)
# This script starts the FastAPI backend on localhost:8000

echo "Starting PM Backend Server..."
echo ""

# Check if we're in the right directory
if [ ! -f "backend/main.py" ]; then
    echo "Error: backend/main.py not found"
    echo "Please run this script from the project root directory"
    exit 1
fi

# Install dependencies if needed
echo "Installing dependencies..."
python3 -m pip install -r backend/requirements.txt

# Start the server
echo ""
echo "Starting uvicorn server on http://127.0.0.1:8000"
echo "Press Ctrl+C to stop the server"
echo ""

python3 -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
