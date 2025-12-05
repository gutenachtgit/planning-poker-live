#!/bin/bash

echo "🎴 Planning Poker starten..."

cleanup() {
    echo ""
    echo "🛑 Server stoppen..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    exit 0
}

trap cleanup SIGINT SIGTERM

cd "$(dirname "$0")"

echo "📦 Backend starten (Port 8001)..."
cd backend
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8001 &
BACKEND_PID=$!
cd ..

sleep 2

echo "🖥️  Frontend starten (Port 5173)..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

sleep 3

echo ""
echo "✅ Planning Poker laeuft!"
echo ""
echo "   Frontend: http://localhost:5173"
echo "   Backend:  http://localhost:8001"
echo ""
echo "   Druecke Ctrl+C zum Beenden"
echo ""

wait
