from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from pydantic import BaseModel
from datetime import datetime

from model import predict_text, MODEL_VERSION, MODEL_ACCURACY
from database import store_flag
from auth import (
    hash_password,
    verify_password,
    create_access_token,
    decode_access_token,
)

# -----------------------------
# App
# -----------------------------
app = FastAPI(title="Fake Job Detection API", version="1.0")

# -----------------------------
# CORS (FIXED)
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],          # includes OPTIONS
    allow_headers=["*"],          # includes Authorization
)

# -----------------------------
# Admin credentials
# -----------------------------
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD_HASH = hash_password("admin123")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# -----------------------------
# Schemas
# -----------------------------
class PredictRequest(BaseModel):
    text: str

class FlagRequest(BaseModel):
    job_text: str
    reason: str
    comments: str = ""
    email: str = ""

class PredictResponse(BaseModel):
    prediction: str
    confidence: float
    processing_time: float
    timestamp: str

class StatusResponse(BaseModel):
    status: str

# -----------------------------
# Auth dependency (ALLOW OPTIONS)
# -----------------------------
def get_current_admin(
    request: Request,
    token: str = Depends(oauth2_scheme),
):
    # ✅ allow browser preflight
    if request.method == "OPTIONS":
        return None

    payload = decode_access_token(token)
    if not payload or payload.get("sub") != ADMIN_USERNAME:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return ADMIN_USERNAME

# -----------------------------
# OPTIONS HANDLERS (CRITICAL)
# -----------------------------
@app.options("/predict")
async def options_predict():
    return {}

@app.options("/flag")
async def options_flag():
    return {}

@app.options("/model-info")
async def options_model_info():
    return {}

# -----------------------------
# Routes
# -----------------------------
@app.get("/", response_model=StatusResponse)
def home():
    return {"status": "API running"}

@app.get("/health", response_model=StatusResponse)
def health():
    return {"status": "Healthy"}

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if (
        form_data.username != ADMIN_USERNAME
        or not verify_password(form_data.password, ADMIN_PASSWORD_HASH)
    ):
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    token = create_access_token({"sub": ADMIN_USERNAME})
    return {"access_token": token, "token_type": "bearer"}

@app.get("/model-info", dependencies=[Depends(get_current_admin)])
def model_info():
    return {
        "version": MODEL_VERSION,
        "accuracy": MODEL_ACCURACY,
    }

@app.post(
    "/predict",
    response_model=PredictResponse,
    dependencies=[Depends(get_current_admin)],
)
def predict(request: PredictRequest):
    if len(request.text.strip()) < 20:
        raise HTTPException(status_code=400, detail="Text too short")

    result = predict_text(request.text)

    return {
        "prediction": result["label"],
        "confidence": result["confidence"],
        "processing_time": result["processing_time"],
        "timestamp": datetime.now().isoformat(),
    }

@app.post("/flag", dependencies=[Depends(get_cur_]()
