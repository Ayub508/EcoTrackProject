import numpy as np
import pandas as pd
import joblib
import os
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score


FEATURE_COLS = [
    'transport_avg_4w', 'energy_avg_4w', 'diet_avg_4w', 'consumption_avg_4w',
    'total_avg_4w', 'transport_change', 'energy_change', 'diet_change',
    'consumption_change', 'total_change', 'month', 'activity_frequency'
]

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'saved_models', 'carbon_predictor.joblib')


def train(data_path=None):
    if data_path is None:
        data_path = os.path.join(os.path.dirname(__file__), 'data', 'prediction_features.csv')

    df = pd.read_csv(data_path)
    X = df[FEATURE_COLS]
    y = df['target_co2']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = GradientBoostingRegressor(
        n_estimators=200,
        max_depth=5,
        learning_rate=0.1,
        min_samples_split=10,
        min_samples_leaf=5,
        random_state=42
    )
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print(f"Carbon Predictor - MAE: {mae:.3f}, R²: {r2:.3f}")

    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    print(f"Model saved to {MODEL_PATH}")

    return model, {'mae': mae, 'r2': r2}


def predict(features):
    model = joblib.load(MODEL_PATH)

    if isinstance(features, dict):
        features = pd.DataFrame([features])

    for col in FEATURE_COLS:
        if col not in features.columns:
            features[col] = 0

    prediction = model.predict(features[FEATURE_COLS])
    return float(max(0, prediction[0]))


if __name__ == '__main__':
    train()
