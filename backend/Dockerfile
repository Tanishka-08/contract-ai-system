FROM python:3.9-slim

WORKDIR /app

# Install system dependencies (needed for psycopg2)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the backend code into a backend/ folder inside /app
COPY backend/ ./backend/

# Run FastAPI with Uvicorn, treating backend as a package
# We use shell form to allow variable substitution for Render's PORT
CMD uvicorn backend.main:app --host 0.0.0.0 --port ${PORT:-8000}
