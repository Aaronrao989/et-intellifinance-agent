#!/usr/bin/env bash

# Exit on error
set -o errexit

echo "🚀 Starting ET IntelliFinance Backend..."

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Run FastAPI with Gunicorn (production-ready)
gunicorn app.api:app \
    --workers 2 \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind 0.0.0.0:$PORT