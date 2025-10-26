# backend/train_model.py
import os
import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import joblib

os.makedirs("backend/model", exist_ok=True)

def generate_synthetic_data(days=400):
    rows = []
    rng = np.random.RandomState(42)
    for day in range(days):
        for hour in range(24):
            base = 2.0 + np.sin(hour * np.pi / 12) * 1.5
            noise = rng.normal(0, 0.2)
            consumption = max(0.1, base + noise)
            generation = 0.0
            if 6 < hour < 19:
                generation = max(0.0, 3.0 * np.sin((hour - 6) * np.pi / 13) + rng.normal(0, 0.2))
            net = consumption - generation
            is_weekend = int((day % 7) in (5, 6))
            rows.append({
                "day": day,
                "hour": hour,
                "consumption": consumption,
                "generation": generation,
                "net": net,
                "is_weekend": is_weekend
            })
    return pd.DataFrame(rows)

if __name__ == "__main__":
    print("Generating synthetic data...")
    df = generate_synthetic_data(days=400)

    # Feature engineering
    df["hour_sin"] = np.sin(df["hour"] * 2 * np.pi / 24)
    df["hour_cos"] = np.cos(df["hour"] * 2 * np.pi / 24)

    features = ["hour", "hour_sin", "hour_cos", "is_weekend", "generation"]
    target = "consumption"

    X = df[features]
    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15, random_state=42)

    print("Training GradientBoostingRegressor...")
    model = GradientBoostingRegressor(n_estimators=200, learning_rate=0.05, max_depth=5, random_state=42)
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    mae = mean_absolute_error(y_test, preds)
    print(f"Model MAE: {mae:.3f} kW")

    model_path = "backend/model/energy_model.joblib"
    joblib.dump(model, model_path)
    print(f"Saved model to {model_path}")

    # Save a small CSV of last 7 days (useful for /api/history)
    df_sample = df.tail(24 * 7)
    df_sample.to_csv("backend/history_sample.csv", index=False)
    print("Saved sample history to backend/history_sample.csv")
