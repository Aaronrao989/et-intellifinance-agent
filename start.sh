#!/usr/bin/env bash

set -o errexit

echo "🚀 Starting ET IntelliFinance Backend..."

# Start server
gunicorn app.api:app \
    --workers 2 \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind 0.0.0.0:$PORT