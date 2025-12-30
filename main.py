from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
from model import predict_text, MODEL_VERSION, MODEL_ACCURACY
from database import store_flag

app = FastAPI(title="Fake Job Detection API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class PredictRequest(BaseModel):
    text: str

class FlagRequest(BaseModel):
    job_text: str
    reason: str
    comments: str = ""
    email: str = ""

@app.get("/")
def home():
    return {"status": "API running"}

@app.get("/health")
def health():
    return {"status": "Healthy"}

@app.get("/model-info")
def model_info():
    return {"version": MODEL_VERSION, "accuracy": MODEL_ACCURACY}

@app.post("/predict")
def predict(request: PredictRequest):
    if len(request.text.strip()) < 20:
        raise HTTPException(status_code=400, detail="Text too short")

    result = predict_text(request.text)

    return {
        "label": result["label"],                 # ✅ clean key
        "confidence": result["confidence"],       # ✅ number
        "processing_time": result["processing_time"],  # ✅ number
        "timestamp": datetime.now().isoformat()
    }

@app.post("/flag")
def flag_post(request: FlagRequest):
    data = request.dict()
    data["timestamp"] = datetime.now().isoformat()
    store_flag(data)
    return {"message": "Post flagged successfully"}
