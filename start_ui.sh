#!/bin/bash

echo "🎨 Starting Streamlit UI for Loan Approval System..."
echo ""

cd "$(dirname "$0")"

# Export Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

echo "✅ UI starting on http://127.0.0.1:8501"
echo ""
echo "Make sure FastAPI backend is running on http://127.0.0.1:8000"
echo ""
echo "Press Ctrl+C to stop"
echo ""

streamlit run ui/chatbot.py --server.port=8501 --server.address=127.0.0.1
