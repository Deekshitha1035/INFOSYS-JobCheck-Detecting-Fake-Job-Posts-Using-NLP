from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import Dict
import sqlite3
import csv
import io
from datetime import timedelta

from auth import (
    hash_password,
    verify_password,
    create_access_token,
    decode_access_token
)

# ================= DATABASE =================
DB_NAME = "database.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        role TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS jobs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT,
        prediction TEXT,
        confidence INTEGER,
        username TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()

# ================= APP =================
app = FastAPI(title="Fake Job Detection API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()

# ================= SCHEMAS =================
class UserCreate(BaseModel):
    username: str
    password: str

class PredictRequest(BaseModel):
    text: str

# ================= SECURITY =================
security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Dict:
    token = credentials.credentials
    user = decode_access_token(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return user

def admin_required(user: Dict):
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin only")
    return user

# ================= AUTH =================
@app.post("/signup")
def signup(user: UserCreate):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM users")
    is_first = cursor.fetchone()[0] == 0
    role = "admin" if is_first else "user"

    try:
        cursor.execute(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            (user.username, hash_password(user.password), role)
        )
        conn.commit()
        return {"message": "Signup successful", "role": role}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Username already exists")
    finally:
        conn.close()

@app.post("/login")
def login(user: UserCreate):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT username, password, role FROM users WHERE username=?",
        (user.username,)
    )
    db_user = cursor.fetchone()
    conn.close()

    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(
        {"username": db_user["username"], "role": db_user["role"]},
        expires_delta=timedelta(minutes=30)
    )

    return {
        "access_token": token,
        "token_type": "Bearer",
        "role": db_user["role"]
    }

# ================= PREDICT =================
@app.post("/predict")
def predict(
    request: PredictRequest,
    user: Dict = Depends(get_current_user)
):
    text = request.text.lower()

    fake_keywords = [
        "pay registration fee",
        "whatsapp",
        "telegram",
        "work from home",
        "no interview",
        "urgent hiring",
        "limited slots",
        "earn per day",
        "click here",
        "processing fee",
        "contact immediately",
        "gmail.com",
        "free training",
        "no experience required",
        "Apply immediately",
        "Limited slots",
        "Final chance today",
        "Registration fees",
        "Training fees",
        "Security deposits",
        "Earn money fast",
        "High income",
        "Unlimited earnings",
        "Guaranteed salary"
    ]

    real_keywords = [
        "job description",
        "roles and responsibilities",
        "qualifications",
        "experience",
        "ctc",
        "full-time",
        "company",
        "location",
        "interview process",
        "skills required",
        "bonus","insurance","ctc"
    ]

    fake_score = sum(1 for k in fake_keywords if k in text)
    real_score = sum(1 for k in real_keywords if k in text)

    if fake_score > real_score:
        prediction = "Fake"
        confidence = min(95, 60 + fake_score * 5)
    else:
        prediction = "Real"
        confidence = min(95, 60 + real_score * 5)

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO jobs (text, prediction, confidence, username)
        VALUES (?, ?, ?, ?)
    """, (
        request.text,
        prediction,
        confidence,
        user["username"]
    ))

    conn.commit()
    conn.close()

    return {
        "prediction": prediction,
        "confidence": confidence
    }

# ================= ADMIN =================
@app.get("/admin/predictions/history")
def history(user: Dict = Depends(get_current_user)):
    admin_required(user)

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, username, prediction, confidence, created_at
        FROM jobs
        ORDER BY created_at DESC
    """)

    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]

@app.get("/admin/predictions/stats")
def stats(user: Dict = Depends(get_current_user)):
    admin_required(user)

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT prediction, COUNT(*) AS count
        FROM jobs
        GROUP BY prediction
    """)

    rows = cursor.fetchall()
    conn.close()

    result = {"Fake": 0, "Real": 0}
    for r in rows:
        result[r["prediction"]] = r["count"]

    return {
        "fake": result["Fake"],
        "real": result["Real"]
    }

@app.get("/admin/predictions/daily")
def daily(user: Dict = Depends(get_current_user)):
    admin_required(user)

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT DATE(created_at) AS day, COUNT(*) AS count
        FROM jobs
        GROUP BY day
        ORDER BY day
    """)

    rows = cursor.fetchall()
    conn.close()

    return {
        "labels": [r["day"] for r in rows],
        "counts": [r["count"] for r in rows]
    }

@app.get("/admin/predictions/confidence")
def confidence(user: Dict = Depends(get_current_user)):
    admin_required(user)

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT confidence, COUNT(*) AS count
        FROM jobs
        GROUP BY confidence
        ORDER BY confidence
    """)

    rows = cursor.fetchall()
    conn.close()

    return {
        "confidence": [r["confidence"] for r in rows],
        "counts": [r["count"] for r in rows]
    }

@app.get("/admin/predictions/export")
def export(user: Dict = Depends(get_current_user)):
    admin_required(user)

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, username, prediction, confidence, created_at
        FROM jobs
    """)

    rows = cursor.fetchall()
    conn.close()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["ID", "Username", "Prediction", "Confidence", "Date"])

    for r in rows:
        writer.writerow([
            r["id"], r["username"], r["prediction"],
            r["confidence"], r["created_at"]
        ])

    output.seek(0)

    return StreamingResponse(
        output,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=predictions.csv"}
    )

# ================= HEALTH =================
@app.get("/health")
def health():
    return {"status": "ok"}

# ================= RUN =================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
