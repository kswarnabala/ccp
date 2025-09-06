from transformers import pipeline
import os
import re

# HuggingFace model (fallback to keyword rules if offline)
MODEL_NAME = os.environ.get("SPAM_MODEL", "bhadresh-savani/bert-base-uncased-emotion")

_classifier = None
try:
    _classifier = pipeline("text-classification", model=MODEL_NAME, tokenizer=MODEL_NAME, device=-1)
except Exception:
    _classifier = None

SPAM_KEYWORDS = [
    r"click here", r"free gift", r"congratulations", r"you (?:won|won't)", r"lottery", r"claim now",
    r"verify your account", r"account has been suspended", r"password will expire", r"urgent action required",
    r"immediate action required", r"free card", r"credit card", r"wire transfer", r"bank account"
]


def keyword_check(text: str) -> bool:
    t = text.lower()
    for pat in SPAM_KEYWORDS:
        if re.search(pat, t):
            return True
    return False


def classify_text(text: str):
    """
    Returns {"label": "SAFE"|"SUSPICIOUS", "score": float}
    Keyword-based + HuggingFace model fallback.
    """
    if not text:
        return {"label": "SAFE", "score": 1.0}

    # Quick keyword hit => suspicious
    if keyword_check(text):
        return {"label": "SUSPICIOUS", "score": 0.99}

    # Use HuggingFace model if available
    if _classifier is not None:
        try:
            short = text if len(text) < 2000 else text[:2000]
            out = _classifier(short[:1000])  # slice for safety
            lbl = out[0]["label"].lower()
            score = float(out[0]["score"])

            # Map labels to safe/suspicious
            suspicious_tokens = ["anger", "fear", "negative", "sadness", "disgust"]
            label = "SUSPICIOUS" if any(tok in lbl for tok in suspicious_tokens) else "SAFE"

            if re.match(r"label_\d+", lbl):  # generic labels (LABEL_0/1)
                label = "SAFE"

            return {"label": label, "score": score}
        except Exception:
            pass

    # Fallback
    return {"label": "SAFE", "score": 0.5}
