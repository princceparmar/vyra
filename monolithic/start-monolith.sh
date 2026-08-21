#!/bin/bash
set -e

echo "=================================================="
echo "      STARTING VYRA MONOLITHIC APPLICATION        "
echo "=================================================="

# Navigate to script directory
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "$DIR/backend"

# Ensure data directory exists
mkdir -p ../data

echo "[1/2] Seeding central database (vyra.db)..."
python3 seed.py

echo "[2/2] Starting Monolithic FastAPI Server on http://localhost:8000 ..."
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
