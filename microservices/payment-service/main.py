import sqlite3
import uuid
import os
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional

DB_PATH = Path(__file__).parent / "database" / "payments.db"

def get_db_connection():
    os.makedirs(DB_PATH.parent, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS payments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        transaction_id TEXT UNIQUE NOT NULL,
        user_id INTEGER NOT NULL,
        amount REAL NOT NULL,
        payment_method TEXT NOT NULL,
        status TEXT NOT NULL, -- SUCCESS, FAILED
        failure_reason TEXT,
        card_last4 TEXT,
        upi_id TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()
    conn.close()

app = FastAPI(title="VYRA Microservice — Payment Service", version="1.0.0")

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

class ProcessPaymentRequest(BaseModel):
    user_id: int = 1
    amount: float
    payment_method: str # Credit Card, Debit Card, UPI, Cash on Delivery
    card_number: Optional[str] = None
    upi_id: Optional[str] = None
    simulate_failure: bool = False

@app.get("/api/health")
def health():
    return {"service": "Payment Service", "status": "healthy", "database": "payments.db", "port": 8015}

@app.post("/api/payment/process")
def process_payment(req: ProcessPaymentRequest):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    tx_id = f"TX-VYRA-{uuid.uuid4().hex[:8].upper()}"

    card_last4 = None
    if req.payment_method in ["Credit Card", "Debit Card"] and req.card_number:
        card_last4 = req.card_number[-4:] if len(req.card_number) >= 4 else req.card_number

    payment_status = "SUCCESS"
    if req.payment_method == "Cash on Delivery":
        payment_status = "Pending"

    if req.simulate_failure:
        cursor.execute("""
        INSERT INTO payments (transaction_id, user_id, amount, payment_method, status, failure_reason, card_last4, upi_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (tx_id, req.user_id, req.amount, req.payment_method, "FAILED", "Simulated decline by issuer bank", card_last4, req.upi_id))
        conn.commit()
        conn.close()
        raise HTTPException(status_code=402, detail="Simulated Payment Failure: Declined by issuing bank.")

    cursor.execute("""
    INSERT INTO payments (transaction_id, user_id, amount, payment_method, status, failure_reason, card_last4, upi_id)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (tx_id, req.user_id, req.amount, req.payment_method, payment_status, None, card_last4, req.upi_id))
    
    conn.commit()
    conn.close()

        "message": "Payment recorded in payments.db",
        "transaction_id": tx_id,
        "amount": req.amount,
        "payment_method": req.payment_method,
        "status": payment_status
    }

@app.get("/api/payment/history/{user_id}")
def get_payment_history(user_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM payments WHERE user_id = ? ORDER BY created_at DESC", (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

gui_path = Path(__file__).parent / "gui" / "index.html"
@app.get("/", response_class=HTMLResponse)
def serve_gui():
    if gui_path.exists():
        with open(gui_path, "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>Payment Service GUI Missing</h1>"
