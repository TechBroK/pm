FROM python:3.13-slim

WORKDIR /app

# Copy backend and prebuilt frontend dist
COPY backend/ ./backend/
COPY frontend/dist/ ./frontend/dist/
COPY .env ./

# Install python dependencies
RUN python -m pip install --no-cache-dir -r backend/requirements.txt

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
