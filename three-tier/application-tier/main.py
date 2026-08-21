import os
import sys
import uuid
import hashlib
from typing import Optional, List
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Import Database Tier
DB_TIER_PATH = Path(__file__).parent.parent / "database-tier"
sys.path.append(str(DB_TIER_PATH))
from db import get_db_connection, init_db_tier
from seed import seed_db_tier

app = FastAPI(title="VYRA Three-Tier Application Tier API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    init_db_tier()
    seed_db_tier()

# Pydantic Schemas
class UserRegister(BaseModel):
    name: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class CartItemAdd(BaseModel):
    user_id: int = 1
    product_id: int
    size: str
    color: str
    quantity: int = 1

class CartItemUpdate(BaseModel):
    cart_item_id: int
    quantity: int

class WishlistAction(BaseModel):
    user_id: int = 1
    product_id: int

class CheckoutRequest(BaseModel):
    user_id: int = 1
    customer_name: str
    email: str
    address: str
    city: str
    zip_code: str
    payment_method: str  # Credit Card, Debit Card, UPI, Cash on Delivery
    card_number: Optional[str] = None
    upi_id: Optional[str] = None
    simulate_failure: bool = False

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

# Tier Status
@app.get("/api/tier-status")
def tier_status():
    return {
        "tier": "Application Tier (Tier 2)",
        "port": 8001,
        "database_tier_connected": True,
        "database_file": "vyra.db"
    }

# Auth Endpoints
@app.post("/api/auth/register")
def register(user: UserRegister):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE email = ?", (user.email,))
    if cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=400, detail="Email already registered")
    
    pwd_hash = hash_password(user.password)
    cursor.execute("INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
                   (user.name, user.email, pwd_hash))
    user_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return {"message": "User registered", "user": {"id": user_id, "name": user.name, "email": user.email}}

@app.post("/api/auth/login")
def login(credentials: UserLogin):
    conn = get_db_connection()
    cursor = conn.cursor()
    pwd_hash = hash_password(credentials.password)
    cursor.execute("SELECT id, name, email FROM users WHERE email = ? AND password_hash = ?", 
                   (credentials.email, pwd_hash))
    row = cursor.fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return {"message": "Login successful", "user": dict(row)}

# Product Catalogue Endpoints
@app.get("/api/products")
def get_products(
    category: Optional[str] = None,
    brand: Optional[str] = None,
    search: Optional[str] = None,
    size: Optional[str] = None,
    color: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    sort_by: Optional[str] = None
):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM products WHERE 1=1"
    params = []

    if category and category.lower() != "all":
        if category == "New Arrivals":
            query += " AND is_new = 1"
        elif category == "Seasonal Collection":
            query += " AND is_seasonal = 1"
        else:
            query += " AND category = ?"
            params.append(category)

    if brand:
        query += " AND brand = ?"
        params.append(brand)

    if search:
        query += " AND (name LIKE ? OR description LIKE ? OR brand LIKE ?)"
        term = f"%{search}%"
        params.extend([term, term, term])

    if size:
        query += " AND sizes LIKE ?"
        params.append(f"%{size}%")

    if color:
        query += " AND colors LIKE ?"
        params.append(f"%{color}%")

    if min_price is not None:
        query += " AND price >= ?"
        params.append(min_price)

    if max_price is not None:
        query += " AND price <= ?"
        params.append(max_price)

    if sort_by == "price_asc":
        query += " ORDER BY price ASC"
    elif sort_by == "price_desc":
        query += " ORDER BY price DESC"
    elif sort_by == "rating":
        query += " ORDER BY rating DESC"
    elif sort_by == "discount":
        query += " ORDER BY discount DESC"
    else:
        query += " ORDER BY id ASC"

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()

    result = []
    for r in rows:
        d = dict(r)
        d["sizes"] = d["sizes"].split(",")
        d["colors"] = d["colors"].split(",")
        d["images"] = d["images"].split("|")
        d["final_price"] = round(d["price"] * (1 - d["discount"] / 100.0), 2)
        result.append(d)

    return result

@app.get("/api/products/{product_id}")
def get_product_detail(product_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Product not found")
    
    d = dict(row)
    d["sizes"] = d["sizes"].split(",")
    d["colors"] = d["colors"].split(",")
    d["images"] = d["images"].split("|")
    d["final_price"] = round(d["price"] * (1 - d["discount"] / 100.0), 2)
    return d

@app.get("/api/categories")
def get_categories():
    return ["All", "Women", "Men", "Footwear", "Accessories", "New Arrivals", "Seasonal Collection"]

# Wishlist Endpoints
@app.get("/api/wishlist/{user_id}")
def get_wishlist(user_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT p.* FROM products p
    JOIN wishlist w ON p.id = w.product_id
    WHERE w.user_id = ?
    """, (user_id,))
    rows = cursor.fetchall()
    conn.close()
    result = []
    for r in rows:
        d = dict(r)
        d["sizes"] = d["sizes"].split(",")
        d["colors"] = d["colors"].split(",")
        d["images"] = d["images"].split("|")
        d["final_price"] = round(d["price"] * (1 - d["discount"] / 100.0), 2)
        result.append(d)
    return result

@app.post("/api/wishlist/toggle")
def toggle_wishlist(item: WishlistAction):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM wishlist WHERE user_id = ? AND product_id = ?", (item.user_id, item.product_id))
    existing = cursor.fetchone()
    if existing:
        cursor.execute("DELETE FROM wishlist WHERE id = ?", (existing["id"],))
        conn.commit()
        conn.close()
        return {"status": "removed", "message": "Product removed from wishlist"}
    else:
        cursor.execute("INSERT INTO wishlist (user_id, product_id) VALUES (?, ?)", (item.user_id, item.product_id))
        conn.commit()
        conn.close()
        return {"status": "added", "message": "Product saved to wishlist"}

# Cart Endpoints
@app.get("/api/cart/{user_id}")
def get_cart(user_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT c.id as cart_id, c.quantity, c.size, c.color, p.*
    FROM cart_items c
    JOIN products p ON c.product_id = p.id
    WHERE c.user_id = ?
    """, (user_id,))
    rows = cursor.fetchall()
    conn.close()

    items = []
    subtotal = 0.0
    total_discount = 0.0

    for r in rows:
        d = dict(r)
        d["sizes"] = d["sizes"].split(",")
        d["colors"] = d["colors"].split(",")
        d["images"] = d["images"].split("|")
        orig_price = d["price"]
        disc = d["discount"]
        final_price = round(orig_price * (1 - disc / 100.0), 2)
        d["final_price"] = final_price
        
        item_subtotal = orig_price * d["quantity"]
        item_final = final_price * d["quantity"]
        subtotal += item_subtotal
        total_discount += (item_subtotal - item_final)
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
        INSERT INTO cart_items (user_id, product_id, size, color, quantity)
        VALUES (?, ?, ?, ?, ?)
        """, (item.user_id, item.product_id, item.size, item.color, item.quantity))
    
    conn.commit()
    conn.close()
    return {"message": "Product added to cart"}

@app.put("/api/cart/update")
def update_cart_item(item: CartItemUpdate):
    conn = get_db_connection()
    cursor = conn.cursor()
    if item.quantity <= 0:
        cursor.execute("DELETE FROM cart_items WHERE id = ?", (item.cart_item_id,))
    else:
        cursor.execute("UPDATE cart_items SET quantity = ? WHERE id = ?", (item.quantity, item.cart_item_id))
    conn.commit()
    conn.close()
    return {"message": "Cart updated"}

@app.delete("/api/cart/remove/{cart_item_id}")
def remove_cart_item(cart_item_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cart_items WHERE id = ?", (cart_item_id,))
    conn.commit()
    conn.close()
    return {"message": "Item removed from cart"}

# Checkout & Orders Endpoints
@app.post("/api/checkout")
def process_checkout(req: CheckoutRequest):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT c.quantity, c.size, c.color, p.id as product_id, p.name, p.brand, p.price, p.discount, p.images
    FROM cart_items c
    JOIN products p ON c.product_id = p.id
    WHERE c.user_id = ?
    """, (req.user_id,))
    cart_rows = cursor.fetchall()

    if not cart_rows:
        conn.close()
        raise HTTPException(status_code=400, detail="Cart is empty")

    if req.simulate_failure:
        conn.close()
        raise HTTPException(status_code=402, detail="Simulated Payment Failure: Payment gateway returned card authorization failure.")

    subtotal = 0.0
    discount_amount = 0.0

    items_to_insert = []
    for r in cart_rows:
        orig_price = r["price"]
        disc = r["discount"]
        final_p = round(orig_price * (1 - disc / 100.0), 2)
        qty = r["quantity"]
        subtotal += orig_price * qty
        discount_amount += (orig_price - final_p) * qty
        
        img_url = r["images"].split("|")[0]
        items_to_insert.append({
            "product_id": r["product_id"],
            "product_name": r["name"],
            "brand": r["brand"],
            "price": final_p,
            "quantity": qty,
            "size": r["size"],
            "color": r["color"],
            "image_url": img_url
        })

    delivery_fee = 0.0 if (subtotal - discount_amount) > 150 else 15.0
    total_amount = round(subtotal - discount_amount + delivery_fee, 2)
    order_number = f"VYRA-3TIER-{uuid.uuid4().hex[:8].upper()}"

    payment_status = "SUCCESS"
    if req.payment_method == "Cash on Delivery":
        payment_status = "Pending"

    cursor.execute("""
    INSERT INTO orders (order_number, user_id, customer_name, email, address, city, zip_code, subtotal, discount_amount, delivery_fee, total_amount, payment_method, payment_status, order_status)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        order_number, req.user_id, req.customer_name, req.email, req.address, req.city, req.zip_code,
        round(subtotal, 2), round(discount_amount, 2), delivery_fee, total_amount,
        req.payment_method, payment_status, "Order Placed"
    ))
    order_id = cursor.lastrowid

    # Insert into payments table
    card_last4 = None
    if req.payment_method in ["Credit Card", "Debit Card"] and req.card_number:
        card_last4 = req.card_number[-4:] if len(req.card_number) >= 4 else req.card_number
    
    transaction_id = f"TXN-{uuid.uuid4().hex[:8].upper()}"

    cursor.execute("""
    INSERT INTO payments (transaction_id, order_id, user_id, payment_method, amount, status, card_last4, upi_id)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        transaction_id, order_id, req.user_id, req.payment_method, total_amount, payment_status, card_last4, req.upi_id
    ))

    for item in items_to_insert:
        cursor.execute("""
        INSERT INTO order_items (order_id, product_id, product_name, brand, price, quantity, size, color, image_url)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            order_id, item["product_id"], item["product_name"], item["brand"],
            item["price"], item["quantity"], item["size"], item["color"], item["image_url"]
        ))

    cursor.execute("DELETE FROM cart_items WHERE user_id = ?", (req.user_id,))
    conn.commit()
    conn.close()

    return {
        "message": "Order processed successfully",
        "order_id": order_id,
        "order_number": order_number,
        "total_amount": total_amount,
        "payment_status": payment_status,
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
        order_dict = dict(o)
        cursor.execute("SELECT * FROM order_items WHERE order_id = ?", (o["id"],))
        order_dict["items"] = [dict(i) for i in cursor.fetchall()]
        result.append(order_dict)

    conn.close()
    return result
