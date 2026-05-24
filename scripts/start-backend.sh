#!/bin/bash
# Start PM Backend Server (macOS/Linux)
# This script builds the frontend and starts the FastAPI backend on localhost:8000

echo "Starting PM Backend Server..."
echo ""

# Check if we're in the right directory
if [ ! -f "backend/main.py" ]; then
    echo "Error: backend/main.py not found"
    echo "Please run this script from the project root directory"
    exit 1
fi

# Build frontend
echo "Building frontend..."
cd frontend
npm install --silent
npm run build
cd ..

if [ $? -ne 0 ]; then
    echo "Error: Frontend build failed"
    exit 1
fi

# Install backend dependencies if needed
echo "Installing backend dependencies..."
python3 -m pip install -q -r backend/requirements.txt

# Start the server
echo ""
echo "Starting uvicorn server on http://127.0.0.1:8000"
echo "Press Ctrl+C to stop the server"
echo ""

python3 -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
