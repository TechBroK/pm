#!/usr/bin/env python
"""
Project Management MVP Backend
FastAPI application serving frontend and API endpoints
"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, FileResponse
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(title="PM Backend", version="0.1.0")

# Determine frontend build path
backend_dir = Path(__file__).parent
project_root = backend_dir.parent
frontend_dist = project_root / "frontend" / "dist"

logger.info(f"Frontend dist path: {frontend_dist}")


@app.get("/api/test")
async def test_endpoint():
    """Simple test endpoint to verify API is working"""
    return JSONResponse({"message": "Hello from API"})


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return JSONResponse({"status": "ok"})


# Mount Next.js static assets
if frontend_dist.exists():
    logger.info("Mounting Next.js static files from frontend/dist")
    app.mount("/_next", StaticFiles(directory=frontend_dist / "_next"), name="next-static")
    
    # Mount all static files from dist
    try:
        app.mount("/", StaticFiles(directory=frontend_dist, html=True), name="static")
        logger.info("Successfully mounted frontend from frontend/dist")
    except Exception as e:
        logger.error(f"Failed to mount frontend: {e}")
else:
    logger.warning(f"Frontend dist not found at {frontend_dist}")
    logger.warning("Run 'npm run build' in frontend/ directory to build the frontend")


if __name__ == "__main__":
    import uvicorn
    
    logger.info("Starting PM Backend server...")
    uvicorn.run(app, host="127.0.0.1", port=8000)
