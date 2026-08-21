#!/usr/bin/env bg-sh
#!/bin/bash
set -e

echo "=================================================="
echo "    STARTING VYRA MICROSERVICES ARCHITECTURE      "
echo "=================================================="

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

echo "[1/6] Starting User Service (Port 8011 & GUI)..."
cd "$DIR/user-service"
python3 -m uvicorn main:app --host 0.0.0.0 --port 8011 --reload &
USER_PID=$!

echo "[2/6] Starting Product Service (Port 8012 & GUI)..."
cd "$DIR/product-service"
python3 -m uvicorn main:app --host 0.0.0.0 --port 8012 --reload &
PROD_PID=$!

echo "[3/6] Starting Cart Service (Port 8013 & GUI)..."
cd "$DIR/cart-service"
python3 -m uvicorn main:app --host 0.0.0.0 --port 8013 --reload &
CART_PID=$!

echo "[4/6] Starting Order Service (Port 8014 & GUI)..."
cd "$DIR/order-service"
python3 -m uvicorn main:app --host 0.0.0.0 --port 8014 --reload &
ORDER_PID=$!

echo "[5/6] Starting Payment Service (Port 8015 & GUI)..."
cd "$DIR/payment-service"
python3 -m uvicorn main:app --host 0.0.0.0 --port 8015 --reload &
PAY_PID=$!

echo "[6/6] Starting VYRA Gateway & Dashboard (Port 8000)..."
cd "$DIR/gateway"
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload &
GATEWAY_PID=$!

echo ""
echo "All 5 Microservices and Gateway started successfully!"
echo "----------------------------------------------------"
echo "• Gateway & Central Hub:  http://localhost:8000"
echo "• User Service GUI:       http://localhost:8011"
echo "• Product Service GUI:    http://localhost:8012"
echo "• Cart Service GUI:       http://localhost:8013"
echo "• Order Service GUI:      http://localhost:8014"
echo "• Payment Service GUI:    http://localhost:8015"
echo "----------------------------------------------------"
echo ""

trap "kill $USER_PID $PROD_PID $CART_PID $ORDER_PID $PAY_PID $GATEWAY_PID" EXIT
wait
