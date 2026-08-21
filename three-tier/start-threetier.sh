#!/usr/bin/env bg-sh
#!/bin/bash
set -e

echo "=================================================="
echo "       STARTING VYRA THREE-TIER APPLICATION       "
echo "=================================================="

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

echo "[1/3] Initializing Database Tier (database-tier/vyra.db)..."
cd "$DIR/database-tier"
python3 seed.py

echo "[2/3] Starting Application Tier (FastAPI Backend on http://localhost:8001)..."
cd "$DIR/application-tier"
python3 -m uvicorn main:app --host 0.0.0.0 --port 8001 --reload &
APP_PID=$!

echo "[3/3] Starting Presentation Tier (GUI HTTP Server on http://localhost:3000)..."
cd "$DIR/presentation-tier/frontend"
python3 -m http.server 3000 &
GUI_PID=$!

echo ""
echo "Three-Tier Application started successfully!"
echo "• Presentation Tier (GUI): http://localhost:3000"
echo "• Application Tier (APIs): http://localhost:8001"
echo "• Database Tier: database-tier/vyra.db"
echo ""

trap "kill $APP_PID $GUI_PID" EXIT
wait
