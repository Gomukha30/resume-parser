# Stage 1: Build frontend
FROM node:18-alpine AS frontend-builder

WORKDIR /app/frontend
COPY resume-parser/package*.json ./
RUN npm install
COPY resume-parser/ .
ENV REACT_APP_API_URL=/api
RUN npm run build

# Stage 2: Build backend
FROM python:3.10-slim AS backend-builder

WORKDIR /app/backend

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download spaCy model
RUN python -m spacy download en_core_web_sm

# Stage 3: Production image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=app.py \
    FLASK_ENV=production \
    PYTHONPATH=/app/backend \
    PORT=5000

# Create a non-root user and set up directory permissions
RUN useradd -m appuser && \
    mkdir -p /app/backend/data /app/frontend/build && \
    chown -R appuser:appuser /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Switch to non-root user
USER appuser
WORKDIR /app/backend

# Copy Python dependencies from builder
COPY --from=backend-builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=backend-builder /usr/local/bin /usr/local/bin
COPY --from=backend-builder /root/.cache /home/appuser/.cache

# Copy backend code
COPY --chown=appuser:appuser backend/ .

# Copy built frontend files from frontend builder
COPY --from=frontend-builder --chown=appuser:appuser /app/frontend/build /app/frontend/build

# Expose the port the app runs on
EXPOSE $PORT

# Command to run the application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "--threads", "2", "app:app"]
