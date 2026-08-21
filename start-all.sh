#!/usr/bin/env bg-sh
#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "$DIR"

echo "=========================================================="
echo "          VYRA — WEAR YOUR STORY (ACADEMIC DEMO)         "
echo "=========================================================="
echo "Select the architecture implementation you wish to launch:"
echo ""
echo "  1) Monolithic Architecture      (Single app on port 8000)"
echo "  2) Three-Tier Architecture      (GUI: 3000 | API: 8001)"
echo "  3) Microservices Architecture   (Gateway: 8000 | Services: 8011-8015)"
echo "  4) Run Health & Sanity Checks"
echo "  5) Exit"
echo ""
read -p "Enter choice [1-5]: " choice

case $choice in
  1)
    echo "Starting Monolithic Architecture..."
    cd "$DIR/monolithic" && ./start-monolith.sh
    ;;
  2)
    echo "Starting Three-Tier Architecture..."
    cd "$DIR/three-tier" && ./start-threetier.sh
    ;;
  3)
    echo "Starting Microservices Architecture..."
    cd "$DIR/microservices" && ./start-microservices.sh
    ;;
  4)
    echo "Running Python environment verification..."
    python3 -c "import fastapi, uvicorn, pydantic, sqlite3; print('✅ Python environment dependencies verified successfully!')"
    ;;
  5)
    echo "Exiting."
    exit 0
    ;;
  *)
    echo "Invalid option."
    exit 1
    ;;
esac
