# Stage 1: Build the Next.js frontend
FROM node:20-slim AS frontend-build

WORKDIR /app

COPY frontend/package.json frontend/package-lock.json ./frontend/
RUN npm ci --prefix frontend

COPY frontend/ ./frontend/
RUN npm run build --prefix frontend

# Stage 2: Python backend runtime
FROM python:3.13-slim

WORKDIR /app

# Set production environment variables
ENV ENVIRONMENT=production \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Copy backend
COPY backend/ ./backend/

# Copy prebuilt frontend assets from stage 1
COPY --from=frontend-build /app/frontend/dist/ ./frontend/dist/

# Install python dependencies
RUN python -m pip install --no-cache-dir -r backend/requirements.txt

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

EXPOSE 8000

# Run with environment variables from .env or container env
CMD ["python", "-m", "uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000", "--log-level", "info"]
