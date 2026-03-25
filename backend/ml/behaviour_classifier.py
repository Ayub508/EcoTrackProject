import numpy as np
import pandas as pd
import joblib
import os
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.preprocessing import LabelEncoder


FEATURE_COLS = [
    'transport_pct', 'energy_pct', 'diet_pct', 'consumption_pct',
    'transport_trend', 'energy_trend', 'diet_trend', 'total_vs_avg_ratio'
]

CLASS_LABELS = ['high_transport', 'high_energy', 'high_diet', 'balanced_high', 'improving']

KMEANS_PATH = os.path.join(os.path.dirname(__file__), 'saved_models', 'kmeans_clusters.joblib')
RF_PATH = os.path.join(os.path.dirname(__file__), 'saved_models', 'behaviour_classifier.joblib')
ENCODER_PATH = os.path.join(os.path.dirname(__file__), 'saved_models', 'label_encoder.joblib')


def train(data_path=None):
    if data_path is None:
        data_path = os.path.join(os.path.dirname(__file__), 'data', 'classification_features.csv')

    df = pd.read_csv(data_path)
    X = df[FEATURE_COLS]
    y = df['behaviour_class']

    le = LabelEncoder()
    le.fit(CLASS_LABELS)
    y_encoded = le.transform(y)

    kmeans = KMeans(n_clusters=5, random_state=42, n_init=10)
    kmeans.fit(X)
    print(f"K-Means inertia: {kmeans.inertia_:.2f}")

    X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

    rf = RandomForestClassifier(
        n_estimators=150,
        max_depth=10,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42
    )
    rf.fit(X_train, y_train)

    y_pred = rf.predict(X_test)
    report = classification_report(y_test, y_pred, target_names=le.classes_)
    print(f"Behaviour Classifier:\n{report}")

    os.makedirs(os.path.dirname(KMEANS_PATH), exist_ok=True)
    joblib.dump(kmeans, KMEANS_PATH)
    joblib.dump(rf, RF_PATH)
    joblib.dump(le, ENCODER_PATH)
    print("Models saved")

    return rf, kmeans, le


def classify(features):
    rf = joblib.load(RF_PATH)
    le = joblib.load(ENCODER_PATH)

    if isinstance(features, dict):
        features = pd.DataFrame([features])

    for col in FEATURE_COLS:
        if col not in features.columns:
            features[col] = 0

    prediction = rf.predict(features[FEATURE_COLS])
    label = le.inverse_transform(prediction)[0]
    probabilities = rf.predict_proba(features[FEATURE_COLS])[0]
    class_probs = {cls: float(prob) for cls, prob in zip(le.classes_, probabilities)}

    return label, class_probs


def get_cluster(features):
    kmeans = joblib.load(KMEANS_PATH)

    if isinstance(features, dict):
        features = pd.DataFrame([features])

    for col in FEATURE_COLS:
        if col not in features.columns:
            features[col] = 0

    cluster = kmeans.predict(features[FEATURE_COLS])
    return int(cluster[0])


if __name__ == '__main__':
    train()
