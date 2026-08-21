import sqlite3
import uuid
import os
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List

DB_PATH = Path(__file__).parent / "database" / "orders.db"

def get_db_connection():
    os.makedirs(DB_PATH.parent, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_number TEXT UNIQUE NOT NULL,
        user_id INTEGER NOT NULL,
        customer_name TEXT NOT NULL,
        email TEXT NOT NULL,
        address TEXT NOT NULL,
        city TEXT NOT NULL,
        zip_code TEXT NOT NULL,
        subtotal REAL NOT NULL,
        discount_amount REAL NOT NULL,
        delivery_fee REAL NOT NULL,
        total_amount REAL NOT NULL,
        payment_method TEXT NOT NULL,
        payment_status TEXT NOT NULL,
        order_status TEXT DEFAULT 'Order Placed',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS order_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        product_name TEXT NOT NULL,
        brand TEXT NOT NULL,
        price REAL NOT NULL,
        quantity INTEGER NOT NULL,
        size TEXT NOT NULL,
        color TEXT NOT NULL,
        image_url TEXT NOT NULL,
        FOREIGN KEY (order_id) REFERENCES orders(id)
    )
    """)
    conn.commit()
    conn.close()

app = FastAPI(title="VYRA Microservice — Order Service", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    init_db()

class OrderItemSchema(BaseModel):
    product_id: int
    product_name: str
    brand: str
    price: float
    quantity: int
    size: str
    color: str
    image_url: str

class CreateOrderRequest(BaseModel):
    user_id: int = 1
    customer_name: str
    email: str
    address: str
    city: str
    zip_code: str
    subtotal: float
    discount_amount: float
    delivery_fee: float
    total_amount: float
    payment_method: str
    payment_status: str = "SUCCESS"
    items: List[OrderItemSchema]

@app.get("/api/health")
def health():
    return {"service": "Order Service", "status": "healthy", "database": "orders.db", "port": 8014}

@app.post("/api/orders/create")
def create_order(req: CreateOrderRequest):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    order_number = f"VYRA-MICRO-{uuid.uuid4().hex[:8].upper()}"

    cursor.execute("""
    INSERT INTO orders (order_number, user_id, customer_name, email, address, city, zip_code, subtotal, discount_amount, delivery_fee, total_amount, payment_method, payment_status, order_status)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        order_number, req.user_id, req.customer_name, req.email, req.address, req.city, req.zip_code,
        req.subtotal, req.discount_amount, req.delivery_fee, req.total_amount,
        req.payment_method, req.payment_status, "Order Placed"
    ))
    order_id = cursor.lastrowid

    for item in req.items:
        cursor.execute("""
        INSERT INTO order_items (order_id, product_id, product_name, brand, price, quantity, size, color, image_url)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            order_id, item.product_id, item.product_name, item.brand,
            item.price, item.quantity, item.size, item.color, item.image_url
        ))

    conn.commit()
    conn.close()

    return {
        "message": "Order created in orders.db",
        "order_id": order_id,
        "order_number": order_number,
        "total_amount": req.total_amount,
        "order_status": "Order Placed"
    }

@app.get("/api/orders/{user_id}")
def get_user_orders(user_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders WHERE user_id = ? ORDER BY created_at DESC", (user_id,))
    orders = cursor.fetchall()

    result = []
    for o in orders:
        od = dict(o)
        cursor.execute("SELECT * FROM order_items WHERE order_id = ?", (o["id"],))
        od["items"] = [dict(i) for i in cursor.fetchall()]
        result.append(od)

    conn.close()
    return result

@app.get("/api/orders/track/{order_number}")
def track_order(order_number: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders WHERE order_number = ?", (order_number,))
    order = cursor.fetchone()
    if not order:
        conn.close()
        raise HTTPException(status_code=404, detail="Order not found")
    
    od = dict(order)
    cursor.execute("SELECT * FROM order_items WHERE order_id = ?", (order["id"],))
    od["items"] = [dict(i) for i in cursor.fetchall()]
    conn.close()
    return od

gui_path = Path(__file__).parent / "gui" / "index.html"
@app.get("/", response_class=HTMLResponse)
def serve_gui():
    if gui_path.exists():
        with open(gui_path, "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>Order Service GUI Missing</h1>"
