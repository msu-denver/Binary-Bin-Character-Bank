# Use official Python slim image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory inside the container
WORKDIR /app

# Install system dependencies (for SQLite, etc.)
RUN apt-get update && apt-get install -y \
    build-essential \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency file and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the Flask source code
COPY src /app/src

# Create data directory (for the SQLite database)
RUN mkdir -p /data

# Expose Flask port
EXPOSE 8008

# Set environment variables for Flask
ENV FLASK_APP=src.app
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=production

# Ensure /data exists as a volume (for persistence)
VOLUME ["/data"]

# Default command to run the Flask app
CMD ["flask", "run", "--host=0.0.0.0", "--port=8008"]
