# backend/app.py
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import joblib
import pandas as pd
import numpy as np
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MODEL_PATH = "backend/model/energy_model.joblib"
model = None
if os.path.exists(MODEL_PATH):
    model = joblib.load(MODEL_PATH)
    print("Model loaded")
else:
    print("Model not found at", MODEL_PATH)

class PredictionRequest(BaseModel):
    base_hour: int  # current hour 0-23
    lookahead: int  # hours ahead to predict
    is_weekend: int = 0

@app.get("/api/history")
def get_history():
    # Return last 24 hours of sample history if present, else synthesize
    csv_path = "backend/history_sample.csv"
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        df24 = df.tail(24)
        out = []
        for _, r in df24.iterrows():
            time = f"{int(r.hour):02d}:00"
            out.append({
                "time": time,
                "consumption": float(r.consumption),
                "generation": float(r.generation)
            })
        return out
    else:
        # fallback synthetic
        rows = []
        for hour in range(24):
            generation = float(max(0, 3 * np.sin((hour - 6) * np.pi / 13)))
            consumption = float(2.0 + np.sin(hour * np.pi / 12) * 1.2)
            rows.append({"time": f"{hour:02d}:00", "consumption": consumption, "generation": generation})
        return rows

@app.post("/api/predict")
def predict(req: PredictionRequest):
    if model is None:
        return {"error": "model not loaded"}
    results = []
    for i in range(1, req.lookahead + 1):
        hour = (req.base_hour + i) % 24
        hour_sin = np.sin(hour * 2 * np.pi / 24)
        hour_cos = np.cos(hour * 2 * np.pi / 24)
        generation = float(max(0, 3 * np.sin((hour - 6) * np.pi / 13))) if 6 < hour < 19 else 0.0
        X = [[hour, hour_sin, hour_cos, req.is_weekend, generation]]
        pred = float(model.predict(X)[0])
        # crude confidence proxy
        confidence = round(min(99.9, max(50.0, 95 - abs(12 - hour) + np.random.randn()*2)), 1)
        results.append({
            "time": f"{hour:02d}:00",
            "consumption": round(pred, 3),
            "generation": round(generation, 3),
            "confidence": confidence
        })
    return results


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    