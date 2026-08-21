import sqlite3
import hashlib
import os
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

DB_PATH = Path(__file__).parent / "database" / "users.db"

def get_db_connection():
    os.makedirs(DB_PATH.parent, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()
    
    # Seed default user if empty
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        pwd = hashlib.sha256("vyra2026".encode()).hexdigest()
        cursor.execute("INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
                       ("Elena Rostova", "elena@vyra.fashion", pwd))
        cursor.execute("INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
                       ("Marcus Vance", "marcus@vyra.fashion", pwd))
        conn.commit()
    conn.close()

app = FastAPI(title="VYRA Microservice — User Service", version="1.0.0")

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

class UserRegister(BaseModel):
    name: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

@app.get("/api/health")
def health():
    return {"service": "User Service", "status": "healthy", "database": "users.db", "port": 8011}

@app.post("/api/users/register")
def register(user: UserRegister):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE email = ?", (user.email,))
    if cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=400, detail="Email already exists")
    
    pwd_hash = hash_password(user.password)
    cursor.execute("INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
                   (user.name, user.email, pwd_hash))
    user_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return {"message": "User registered", "user": {"id": user_id, "name": user.name, "email": user.email}}

@app.post("/api/users/login")
def login(credentials: UserLogin):
    conn = get_db_connection()
    cursor = conn.cursor()
    pwd_hash = hash_password(credentials.password)
    cursor.execute("SELECT id, name, email, created_at FROM users WHERE email = ? AND password_hash = ?", 
                   (credentials.email, pwd_hash))
    user = cursor.fetchone()
    conn.close()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return {"message": "Login successful", "user": dict(user)}

@app.get("/api/users/{user_id}")
def get_user(user_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, email, created_at FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return dict(user)

# Standalone GUI for User Service
gui_path = Path(__file__).parent / "gui" / "index.html"
@app.get("/", response_class=HTMLResponse)
def serve_gui():
    if gui_path.exists():
        with open(gui_path, "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>User Service GUI Missing</h1>"
