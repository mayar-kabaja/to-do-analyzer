"""
To-do analyzer API: load trained models and predict priority + category for task text.

Run from the backend directory:
  cd backend && uvicorn api:app --reload

Then e.g. POST http://127.0.0.1:8000/predict with body {"text": "Buy groceries"}
"""

import os
import pickle

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="To-Do Analyzer API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load models once at startup
_MODELS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "models")

with open(os.path.join(_MODELS_DIR, "vectorizer.pkl"), "rb") as f:
    vectorizer = pickle.load(f)
with open(os.path.join(_MODELS_DIR, "priority_model.pkl"), "rb") as f:
    priority_model = pickle.load(f)
with open(os.path.join(_MODELS_DIR, "category_model.pkl"), "rb") as f:
    category_model = pickle.load(f)


class PredictRequest(BaseModel):
    text: str


class PredictResponse(BaseModel):
    text: str
    priority: str
    category: str


@app.get("/")
def root():
    return {"message": "To-Do Analyzer API", "docs": "/docs"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest):
    """Predict priority and category for a single task text."""
    X_vec = vectorizer.transform([req.text])
    priority = priority_model.predict(X_vec)[0]
    category = category_model.predict(X_vec)[0]
    return PredictResponse(text=req.text, priority=priority, category=category)


class PredictBulkRequest(BaseModel):
    texts: list[str]


class PredictBulkResponse(BaseModel):
    results: list[PredictResponse]


@app.post("/predict_bulk", response_model=PredictBulkResponse)
def predict_bulk(req: PredictBulkRequest):
    """Predict priority and category for multiple task texts in one call."""
    if not req.texts:
        return PredictBulkResponse(results=[])
    X_vec = vectorizer.transform(req.texts)
    priorities = priority_model.predict(X_vec)
    categories = category_model.predict(X_vec)
    results = [
        PredictResponse(text=t, priority=p, category=c)
        for t, p, c in zip(req.texts, priorities, categories)
    ]
    return PredictBulkResponse(results=results)
