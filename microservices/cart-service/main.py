import sqlite3
import os
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

DB_PATH = Path(__file__).parent / "database" / "cart.db"

def get_db_connection():
    os.makedirs(DB_PATH.parent, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cart_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        product_name TEXT NOT NULL,
        brand TEXT NOT NULL,
        price REAL NOT NULL,
        discount INTEGER DEFAULT 0,
        size TEXT NOT NULL,
        color TEXT NOT NULL,
        quantity INTEGER NOT NULL DEFAULT 1,
        image_url TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(user_id, product_id, size, color)
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS wishlist_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        product_name TEXT NOT NULL,
        brand TEXT NOT NULL,
        price REAL NOT NULL,
        discount INTEGER DEFAULT 0,
        image_url TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(user_id, product_id)
    )
    """)
    conn.commit()
    conn.close()

app = FastAPI(title="VYRA Microservice — Cart & Wishlist Service", version="1.0.0")

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

class CartItemAdd(BaseModel):
    user_id: int = 1
    product_id: int
    product_name: str
    brand: str
    price: float
    discount: int = 0
    size: str
    color: str
    quantity: int = 1
    image_url: str

class CartItemUpdate(BaseModel):
    cart_item_id: int
    quantity: int

class WishlistAdd(BaseModel):
    user_id: int = 1
    product_id: int
    product_name: str
    brand: str
    price: float
    discount: int = 0
    image_url: str

@app.get("/api/health")
def health():
    return {"service": "Cart & Wishlist Service", "status": "healthy", "database": "cart.db", "port": 8013}

@app.get("/api/cart/{user_id}")
def get_cart(user_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cart_items WHERE user_id = ?", (user_id,))
    rows = cursor.fetchall()
    conn.close()

    items = []
    subtotal = 0.0
    total_discount = 0.0

    for r in rows:
        d = dict(r)
        orig_p = d["price"]
        disc = d["discount"]
        final_p = round(orig_p * (1 - disc / 100.0), 2)
        d["final_price"] = final_p
        
        qty = d["quantity"]
        subtotal += orig_p * qty
        total_discount += (orig_p - final_p) * qty
        items.append(d)

    final_total = subtotal - total_discount
    return {
        "items": items,
        "subtotal": round(subtotal, 2),
        "total_discount": round(total_discount, 2),
        "final_total": round(final_total, 2)
    }

@app.post("/api/cart/add")
def add_to_cart(item: CartItemAdd):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT id, quantity FROM cart_items 
    WHERE user_id = ? AND product_id = ? AND size = ? AND color = ?
    """, (item.user_id, item.product_id, item.size, item.color))
    existing = cursor.fetchone()

    if existing:
        new_qty = existing["quantity"] + item.quantity
        cursor.execute("UPDATE cart_items SET quantity = ? WHERE id = ?", (new_qty, existing["id"]))
    else:
        cursor.execute("""
        INSERT INTO cart_items (user_id, product_id, product_name, brand, price, discount, size, color, quantity, image_url)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (item.user_id, item.product_id, item.product_name, item.brand, item.price, item.discount, item.size, item.color, item.quantity, item.image_url))
    
    conn.commit()
    conn.close()
    return {"message": "Added to cart in cart.db"}

@app.put("/api/cart/update")
def update_cart(item: CartItemUpdate):
    conn = get_db_connection()
    cursor = conn.cursor()
    if item.quantity <= 0:
        cursor.execute("DELETE FROM cart_items WHERE id = ?", (item.cart_item_id,))
    else:
        cursor.execute("UPDATE cart_items SET quantity = ? WHERE id = ?", (item.quantity, item.cart_item_id))
    conn.commit()
    conn.close()
    return {"message": "Cart updated"}

@app.delete("/api/cart/remove/{cart_id}")
def remove_cart(cart_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cart_items WHERE id = ?", (cart_id,))
    conn.commit()
    conn.close()
    return {"message": "Item removed from cart.db"}

@app.delete("/api/cart/clear/{user_id}")
def clear_cart(user_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cart_items WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()
    return {"message": "Cart cleared"}

@app.get("/api/wishlist/{user_id}")
def get_wishlist(user_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM wishlist_items WHERE user_id = ?", (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

@app.post("/api/wishlist/toggle")
def toggle_wishlist(item: WishlistAdd):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM wishlist_items WHERE user_id = ? AND product_id = ?", (item.user_id, item.product_id))
    existing = cursor.fetchone()
    if existing:
        cursor.execute("DELETE FROM wishlist_items WHERE id = ?", (existing["id"],))
        conn.commit()
        conn.close()
        return {"status": "removed", "message": "Item removed from wishlist in cart.db"}
    else:
        cursor.execute("""
        INSERT INTO wishlist_items (user_id, product_id, product_name, brand, price, discount, image_url)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (item.user_id, item.product_id, item.product_name, item.brand, item.price, item.discount, item.image_url))
        conn.commit()
        conn.close()
        return {"status": "added", "message": "Item saved to wishlist in cart.db"}

gui_path = Path(__file__).parent / "gui" / "index.html"
@app.get("/", response_class=HTMLResponse)
def serve_gui():
    if gui_path.exists():
        with open(gui_path, "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>Cart Service GUI Missing</h1>"
