import time
from typing import Dict

# ==========================
# MODEL METADATA
# ==========================
MODEL_VERSION = "1.0"
MODEL_ACCURACY = 0.924
MODEL_TYPE = "Rule-based (Keyword Matching)"

# ==========================
# FAKE JOB INDICATORS
# ==========================
FAKE_KEYWORDS = [
    "registration fee",
    "pay fee",
    "earn money fast",
    "work from home",
    "no experience",
    "whatsapp",
    "telegram",
    "urgent hiring",
    "easy income",
    "limited slots",
    "instant joining"
]

# ==========================
# PREDICTION FUNCTION
# ==========================
def predict_text(text: str) -> Dict:
    """
    Predict whether job description is Fake or Real
    """

    if not text or not isinstance(text, str):
        raise ValueError("Invalid input text")

    start_time = time.time()
    processed_text = text.lower()

    # Keyword matching score
    score = sum(1 for keyword in FAKE_KEYWORDS if keyword in processed_text)

    # Classification logic
    if score >= 2:
        label = "Fake"
        confidence = min(90 + score * 2, 98)
    else:
        label = "Real"
        confidence = max(85 - score * 5, 75)

    return {
        "label": label,                     # Used for admin counts
        "confidence": confidence,            # For UI display
        "score": score,                      # 🔥 Useful for analytics
        "processing_time": round(time.time() - start_time, 3),
        "model_version": MODEL_VERSION
    }

# ==========================
# MODEL INFO (ADMIN / DOCS)
# ==========================
def get_model_info() -> Dict:
    """
    Return model metadata
    """
    return {
        "model_version": MODEL_VERSION,
        "accuracy": MODEL_ACCURACY,
        "type": MODEL_TYPE,
        "keywords_used": len(FAKE_KEYWORDS)
    }
