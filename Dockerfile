# Dockerfile
# Small updates to use python:3.12-slim as base image

FROM python:3.12-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ src/
COPY app.py app.py

# Copy templates
COPY htmlcov/ /app/htmlcov/

# Create data folder
RUN mkdir -p /app/data

# Flask environment
ENV FLASK_APP=app
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=8008

EXPOSE 8008

CMD ["flask", "run"]
