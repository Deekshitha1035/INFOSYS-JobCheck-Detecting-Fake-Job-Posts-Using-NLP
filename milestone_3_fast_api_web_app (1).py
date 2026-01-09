# Milestone 3 — FastAPI Web App (Notebook-ready Python file)
# Save this file as a .py or paste each cell into Jupyter Notebook cells.
# This script provides all notebook cells needed to implement Milestone 3 (FastAPI backend, frontend, feedback, tests, Docker/requirements).

# -----------------------------
# Cell 1 — Install dependencies (run in a notebook cell or terminal)
# -----------------------------
# !pip install fastapi uvicorn[standard] python-multipart jinja2 aiofiles sqlalchemy pydantic python-dotenv joblib scikit-learn pandas numpy matplotlib seaborn python-docx docx2pdf
# If you plan to use the BiLSTM in the notebook, also install tensorflow compatible with your system.
# !pip install tensorflow==2.13.0

# -----------------------------
# Cell 2 — Imports & basic config
# -----------------------------
import os
import time
import json
import joblib
import sqlite3
from pathlib import Path
from datetime import datetime
from typing import Optional

# FastAPI imports
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from pydantic import BaseModel, Field, validator

# ML & preprocessing imports
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

# Optional: Keras (BiLSTM) - import only if installed & needed
try:
    from tensorflow.keras.models import load_model
    from tensorflow.keras.preprocessing.text import Tokenizer
    from tensorflow.keras.preprocessing.sequence import pad_sequences
    KERAS_AVAILABLE = True
except Exception:
    KERAS_AVAILABLE = False

print('KERAS_AVAILABLE =', KERAS_AVAILABLE)

# -----------------------------
# Cell 3 — Paths and user config
# -----------------------------
BASE_DIR = Path.cwd()
LOGREG_PATH = BASE_DIR / 'logistic_regression_model.pkl'
RF_PATH = BASE_DIR / 'random_forest_model.pkl'
TFIDF_PATH = BASE_DIR / 'tfidf_vectorizer.pkl'
BILSTM_PATH = BASE_DIR / 'bilstm_model.h5'  # optional
DB_PATH = BASE_DIR / 'flags.db'

MODEL_VERSION = 'v1.0'
MODEL_TIMESTAMP = datetime.utcnow().isoformat(timespec='seconds') + 'Z'

# Input validation limits
MIN_TEXT_LENGTH = 20
MAX_TEXT_LENGTH = 20000

print('Base dir:', BASE_DIR)

# -----------------------------
# Cell 4 — Load models (safe)
# -----------------------------
# Attempt to load TF-IDF and sklearn models; BiLSTM optional

tfidf = None
best_lr = None
best_rf = None
bilstm_model = None

if TFIDF_PATH.exists():
    try:
        tfidf = joblib.load(TFIDF_PATH)
        print('Loaded TF-IDF vectorizer')
    except Exception as e:
        print('Failed to load TF-IDF:', e)

if LOGREG_PATH.exists():
    try:
        best_lr = joblib.load(LOGREG_PATH)
        print('Loaded Logistic Regression model')
    except Exception as e:
        print('Failed to load Logistic Regression:', e)

if RF_PATH.exists():
    try:
        best_rf = joblib.load(RF_PATH)
        print('Loaded Random Forest model')
    except Exception as e:
        print('Failed to load Random Forest:', e)

if KERAS_AVAILABLE and BILSTM_PATH.exists():
    try:
        bilstm_model = load_model(str(BILSTM_PATH))
        print('Loaded BiLSTM model')
    except Exception as e:
        print('Failed to load BiLSTM:', e)

if not any([best_lr, best_rf, bilstm_model]):
    print('Warning: No model loaded. Place your model files in the working directory or update the paths.')

# -----------------------------
# Cell 5 — SQLite setup for flags/feedback
# -----------------------------
conn = sqlite3.connect(str(DB_PATH))
cur = conn.cursor()
cur.execute('''
CREATE TABLE IF NOT EXISTS flags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    job_text TEXT,
    reason TEXT,
    comments TEXT,
    user_email TEXT
)
''')
conn.commit()
conn.close()
print('Flag DB ready at', DB_PATH)

# -----------------------------
# Cell 6 — FastAPI app, Pydantic schemas, helper prediction function
# -----------------------------
app = FastAPI(title='Fake Job Detector API', version=MODEL_VERSION)

# Allow CORS for local development; restrict in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PredictRequest(BaseModel):
    text: str = Field(..., description='Job description text')
    meta: Optional[dict] = None

    @validator('text')
    def validate_text(cls, v):
        if not isinstance(v, str):
            raise ValueError('text must be a string')
        if len(v) < MIN_TEXT_LENGTH:
            raise ValueError(f'text too short (min {MIN_TEXT_LENGTH} chars)')
        if len(v) > MAX_TEXT_LENGTH:
            raise ValueError(f'text too long (max {MAX_TEXT_LENGTH} chars)')
        return v

class PredictResponse(BaseModel):
    label: str
    confidence: float
    processing_time_ms: int
    timestamp: str
    model: str

class FlagRequest(BaseModel):
    job_text: str
    reason: str
    comments: Optional[str] = None
    user_email: Optional[str] = None

# Helper prediction function: prefer RF -> LR -> BiLSTM

def predict_text(text: str):
    start = time.time()
    model_used = None
    label = None
    confidence = None

    # Random Forest
    if best_rf is not None and tfidf is not None:
        try:
            x = tfidf.transform([text])
            prob = best_rf.predict_proba(x)[0][1]
            confidence = float(prob * 100)
            label = 'Fake' if prob >= 0.5 else 'Real'
            model_used = 'RandomForest'
        except Exception:
            model_used = None

    # Logistic Regression fallback
    if model_used is None and best_lr is not None and tfidf is not None:
        try:
            x = tfidf.transform([text])
            prob = best_lr.predict_proba(x)[0][1]
            confidence = float(prob * 100)
            label = 'Fake' if prob >= 0.5 else 'Real'
            model_used = 'LogisticRegression'
        except Exception:
            model_used = None

    # BiLSTM fallback
    if model_used is None and bilstm_model is not None:
        tokenizer = globals().get('tokenizer', None)
        max_len = globals().get('max_len', 200)
        if tokenizer is not None:
            seq = tokenizer.texts_to_sequences([text])
            x = pad_sequences(seq, maxlen=max_len)
            prob = float(bilstm_model.predict(x).ravel()[0])
            confidence = float(prob * 100)
            label = 'Fake' if prob >= 0.5 else 'Real'
            model_used = 'BiLSTM'

    if model_used is None:
        raise RuntimeError('No valid model available for prediction.')

    end = time.time()
    return {
        'label': label,
        'confidence': round(confidence, 2),
        'processing_time_ms': int((end - start) * 1000),
        'timestamp': datetime.utcnow().isoformat(timespec='seconds') + 'Z',
        'model': model_used
    }

# -----------------------------
# Cell 7 — FastAPI endpoints
# -----------------------------
@app.get('/health')
async def health():
    return {'status': 'ok', 'timestamp': datetime.utcnow().isoformat(timespec='seconds') + 'Z'}

@app.get('/model_info')
async def model_info():
    return {
        'version': MODEL_VERSION,
        'loaded_models': {
            'logistic_regression': bool(best_lr),
            'random_forest': bool(best_rf),
            'bilstm': bool(bilstm_model)
        },
        'timestamp': MODEL_TIMESTAMP
    }

@app.post('/predict', response_model=PredictResponse)
async def predict(req: PredictRequest):
    try:
        out = predict_text(req.text)
        return JSONResponse(content=out)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except RuntimeError as re:
        raise HTTPException(status_code=503, detail=str(re))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post('/flag')
async def flag_post(payload: FlagRequest):
    try:
        conn = sqlite3.connect(str(DB_PATH))
        cur = conn.cursor()
        cur.execute(
            'INSERT INTO flags (timestamp, job_text, reason, comments, user_email) VALUES (?, ?, ?, ?, ?)',
            (datetime.utcnow().isoformat(timespec='seconds') + 'Z', payload.job_text, payload.reason, payload.comments, payload.user_email)
        )
        conn.commit()
        conn.close()
        return {'status': 'success', 'message': 'Flag saved. Thank you.'}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/flags')
async def get_flags():
    try:
        conn = sqlite3.connect(str(DB_PATH))
        cur = conn.cursor()
        cur.execute('SELECT id, timestamp, reason, comments, user_email, job_text FROM flags ORDER BY id DESC')
        rows = cur.fetchall()
        conn.close()
        keys = ['id', 'timestamp', 'reason', 'comments', 'user_email', 'job_text']
        return [dict(zip(keys, r)) for r in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# -----------------------------
# Cell 8 — Simple frontend (served by API)
# -----------------------------
FRONTEND_HTML = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8"/>
  <title>Fake Job Detector</title>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <style>
    body{font-family:Arial,Helvetica,sans-serif;max-width:900px;margin:20px auto;padding:10px;}
    textarea{width:100%;height:200px;padding:8px;font-size:14px;}
    .btn{padding:10px 16px;margin:6px;border:none;border-radius:6px;cursor:pointer;}
    .btn-primary{background:#007bff;color:white;}
    .btn-danger{background:#dc3545;color:white;}
    .result{margin-top:16px;padding:12px;border-radius:6px;}
    .real{background:#e6ffed;border:1px solid #2ecc71;color:#2ecc71;}
    .fake{background:#ffeef0;border:1px solid #e74c3c;color:#e74c3c;}
    .low{background:#fff7e6;border:1px solid #f39c12;color:#f39c12;}
  </style>
</head>
<body>
<h2>Fake Job Postings Detector</h2>
<p>Paste a job description and click Predict.</p>

<label>Job description</label>
<textarea id="jobtext" placeholder="Paste job description here..."></textarea>
<div>
  <button class="btn btn-primary" onclick="predict()">Predict</button>
  <button class="btn" onclick="document.getElementById('jobtext').value=''">Clear</button>
</div>

<div id="status" style="margin-top:10px;"></div>
<div id="result"></div>

<script>
async function predict(){
  const text = document.getElementById('jobtext').value;
  if(!text || text.length < 20){
    alert('Please enter at least 20 characters.');
    return;
  }
  document.getElementById('status').innerText = 'Processing...';
  document.getElementById('result').innerHTML = '';
  try{
    const resp = await fetch('/predict', {
      method:'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({ text: text })
    });
    if(!resp.ok){
      const err = await resp.json();
      document.getElementById('status').innerText = 'Error: ' + (err.detail || resp.statusText);
      return;
    }
    const data = await resp.json();
    document.getElementById('status').innerText = '';
    let cls = 'low';
    if(data.confidence >= 75) cls = data.label === 'Fake' ? 'fake' : 'real';
    let html = `<div class="result ${cls}"><strong>Prediction:</strong> ${data.label}<br/>
                <strong>Confidence:</strong> ${data.confidence.toFixed(2)}%<br/>
                <strong>Processing time:</strong> ${data.processing_time_ms} ms<br/>
                <strong>Model:</strong> ${data.model}<br/>
                <small>${data.timestamp}</small>
                </div>`;
    document.getElementById('result').innerHTML = html;
  } catch (e){
    document.getElementById('status').innerText = 'Request failed: ' + e;
  }
}
</script>
</body>
</html>
"""

@app.get('/', response_class=HTMLResponse)
async def home():
    return HTMLResponse(content=FRONTEND_HTML, status_code=200)

# -----------------------------
# Cell 9 — Run server (development) from notebook
# -----------------------------
# In a notebook you can run Uvicorn in a background thread. For production, run via CLI:
# uvicorn this_module:app --host 0.0.0.0 --port 8000 --workers 1

# Example code to start within notebook (uncomment to run):
# import threading, uvicorn
# def run_app():
#     uvicorn.run(app, host='127.0.0.1', port=8000, log_level='info')
# t = threading.Thread(target=run_app, daemon=True)
# t.start()
# print('Server running at http://127.0.0.1:8000')

# -----------------------------
# Cell 10 — Integration test (requests)
# -----------------------------
# Use this cell to test predict endpoint after server is running
# import requests
# url = 'http://127.0.0.1:8000/predict'
# sample_text = 'We are hiring an experienced software engineer to join our cloud team. Must know Python and AWS.'
# r = requests.post(url, json={'text': sample_text})
# print(r.status_code, r.json())

# -----------------------------
# Cell 11 — Export helper files: requirements.txt, Dockerfile, README.md
# -----------------------------
requirements = '''
fastapi
uvicorn[standard]
python-multipart
jinja2
aiofiles
sqlalchemy
pydantic
python-dotenv
joblib
scikit-learn
pandas
numpy
matplotlib
seaborn
python-docx
docx2pdf
tensorflow==2.13.0
'''
with open('requirements.txt', 'w') as f:
    f.write(requirements)
print('Wrote requirements.txt')

dockerfile = '''
FROM python:3.11-slim
WORKDIR /app
COPY . /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
'''
with open('Dockerfile', 'w') as f:
    f.write(dockerfile)
print('Wrote Dockerfile')

readme = '''
README - Milestone 3 Web App

1. Install dependencies:
   pip install -r requirements.txt

2. Place the following files in this folder:
   - tfidf_vectorizer.pkl
   - random_forest_model.pkl  (or logistic_regression_model.pkl)
   - bilstm_model.h5 (optional)

3. Run the app (development):
   uvicorn app:app --reload --port 8000

4. Open http://127.0.0.1:8000 for frontend or /docs for API docs.
'''
with open('README.md', 'w') as f:
    f.write(readme)
print('Wrote README.md')

# -----------------------------
# End of Notebook file content
# -----------------------------
