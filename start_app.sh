#!/bin/bash

# Cook Assistant Startup Script
echo "🍳 Starting Cook Assistant Application..."
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.10 or higher."
    exit 1
fi

# Check if dependencies are installed
echo "📦 Checking dependencies..."
if ! python3 -c "import fastapi" 2>/dev/null; then
    echo "📥 Installing dependencies..."
    pip install -r requirements.txt
fi

echo ""
echo "✅ Dependencies OK"
echo ""

# Start backend in background
echo "🚀 Starting backend server..."
python3 run_backend.py &
BACKEND_PID=$!

# Wait for backend to start
echo "⏳ Waiting for backend to initialize..."
sleep 3

# Start UI
echo "🎨 Starting UI server..."
python3 run_ui.py &
UI_PID=$!

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✨ Cook Assistant is running!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📡 Backend API: http://localhost:8080"
echo "🌐 Streamlit UI: http://localhost:8501"
echo ""
echo "Press CTRL+C to stop all servers"
echo ""

# Wait for interrupt
trap "echo ''; echo '🛑 Stopping servers...'; kill $BACKEND_PID $UI_PID 2>/dev/null; echo '✅ Done!'; exit 0" INT

# Keep script running
wait

