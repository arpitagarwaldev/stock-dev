#!/bin/bash

# Stock Trading Simulator - Run Script
# This script starts both backend and frontend servers

echo "🚀 Starting Stock Trading Simulator..."

# Check if setup has been run
if [ ! -d "backend/venv" ]; then
    echo "❌ Virtual environment not found. Please run setup first:"
    echo "python setup.py"
    exit 1
fi

# Function to cleanup background processes
cleanup() {
    echo "🛑 Shutting down servers..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Start backend server
echo "🔧 Starting backend server..."
cd backend

# Activate virtual environment and start backend
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    # Windows
    source venv/Scripts/activate
else
    # Unix/Linux/macOS
    source venv/bin/activate
fi

python src/app.py &
BACKEND_PID=$!

cd ..

# Wait a moment for backend to start
sleep 3

# Start frontend server
echo "🌐 Starting frontend server..."
cd frontend

# Check if Python 3 is available
if command -v python3 &> /dev/null; then
    python3 -m http.server 8000 &
elif command -v python &> /dev/null; then
    python -m http.server 8000 &
else
    echo "❌ Python not found. Please install Python to serve the frontend."
    kill $BACKEND_PID
    exit 1
fi

FRONTEND_PID=$!

cd ..

echo "✅ Servers started successfully!"
echo ""
echo "📊 Backend API: http://localhost:5000"
echo "🌐 Frontend: http://localhost:8000"
echo ""
echo "🎯 Open your browser and go to: http://localhost:8000"
echo ""
echo "Press Ctrl+C to stop all servers"

# Wait for background processes
wait