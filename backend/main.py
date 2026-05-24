#!/usr/bin/env python
"""
Project Management MVP Backend
FastAPI application serving static HTML and API endpoints
"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(title="PM Backend", version="0.1.0")

# Create static directory if it doesn't exist
static_dir = os.path.join(os.path.dirname(__file__), "static")
os.makedirs(static_dir, exist_ok=True)


@app.get("/api/test")
async def test_endpoint():
    """Simple test endpoint to verify API is working"""
    return JSONResponse({"message": "Hello from API"})


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return JSONResponse({"status": "ok"})


# Mount static files to serve at root
app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")


if __name__ == "__main__":
    import uvicorn
    
    logger.info("Starting PM Backend server...")
    uvicorn.run(app, host="127.0.0.1", port=8000)
