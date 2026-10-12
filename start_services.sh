#!/bin/bash

echo "🚀 Starting Loan Approval System Services..."
echo ""

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found. Creating from template..."
    cp .env.template .env 2>/dev/null || echo "ANTHROPIC_API_KEY=your_key_here" > .env
    echo "Please update .env with your API key"
fi

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Create logs directory
mkdir -p logs

# Start FastAPI backend
echo "📡 Starting FastAPI Backend on http://127.0.0.1:8000..."
python -m uvicorn backend.app:app --host 127.0.0.1 --port 8000 --reload &
BACKEND_PID=$!

# Wait for backend to start
sleep 3

# Start Streamlit UI
echo "🎨 Starting Streamlit UI on http://127.0.0.1:8501..."
streamlit run ui/chatbot.py --server.port=8501 --server.address=127.0.0.1 &
UI_PID=$!

echo ""
echo "✅ Services Started!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📡 FastAPI Backend: http://127.0.0.1:8000"
echo "   Docs: http://127.0.0.1:8000/docs"
echo ""
echo "🎨 Streamlit UI: http://127.0.0.1:8501"
echo ""
echo "Press Ctrl+C to stop all services"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Wait for both processes
wait $BACKEND_PID $UI_PID

# Cleanup on exit
trap "kill $BACKEND_PID $UI_PID 2>/dev/null" EXIT
