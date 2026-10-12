#!/bin/bash

echo "📡 Starting FastAPI Backend for Loan Approval System..."
echo ""

cd "$(dirname "$0")"

# Create logs directory
mkdir -p logs

# Export Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

echo "✅ Backend starting on http://127.0.0.1:8000"
echo "📚 API Documentation: http://127.0.0.1:8000/docs"
echo ""
echo "Press Ctrl+C to stop"
echo ""

python -m uvicorn backend.app:app --host 127.0.0.1 --port 8000 --reload
