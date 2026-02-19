# Dockerfile for CI/CD Pipeline Sandbox
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p logs data/timeline

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV CI_ENVIRONMENT=docker

# Default command
CMD ["python", "ci_cd/pipeline/ci_runner.py"]
