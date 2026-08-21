import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

app = FastAPI(title="VYRA Microservices Central Gateway & Dashboard", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/gateway/services")
def list_services():
    return [
        {"name": "User Service", "port": 8011, "db": "users.db", "gui": "http://localhost:8011/"},
        {"name": "Product Service", "port": 8012, "db": "products.db", "gui": "http://localhost:8012/"},
        {"name": "Cart & Wishlist Service", "port": 8013, "db": "cart.db", "gui": "http://localhost:8013/"},
        {"name": "Order Service", "port": 8014, "db": "orders.db", "gui": "http://localhost:8014/"},
        {"name": "Payment Service", "port": 8015, "db": "payments.db", "gui": "http://localhost:8015/"}
    ]

gui_path = Path(__file__).parent / "index.html"
@app.get("/", response_class=HTMLResponse)
def serve_gateway_gui():
    if gui_path.exists():
        with open(gui_path, "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>Gateway GUI File Missing</h1>"
