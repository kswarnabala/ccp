import joblib
from typing import Dict
MODEL_PATH="phishing_model.pk1"
VECT_PATH="vectorizer.pk1"
_model=joblib.load(MODEL_PATH)
_vectorizer=joblib.load(VECT_PATH)
def predict_text(text: str)->Dict:
    vec=_vectorizer.transform([text])
    prob=_model.predict_proba(vec)[0][1] if hasattr(_model,"predict_proba") else float(_model.predict(vec)[0])
    label="phishing" if prob>=0.5 else "Safe"
    return {"label":label,"score":float(prob)}