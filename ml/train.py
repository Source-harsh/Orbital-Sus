import pickle
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from dataset import generate_telemetry_dataset

def train_model():
    print("[ML] Generating synthetic dataset...")
    df = generate_telemetry_dataset(num_samples=3000, output_path="telemetry_dataset.csv")

    X = df.drop(columns=["label"])
    y = df["label"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    print("[ML] Training RandomForest Anomaly Classifier...")
    clf = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)
    print("\n[ML] Model Evaluation Report:")
    print(classification_report(y_test, y_pred))

    model_path = "spacecraft_ml_model.pkl"
    with open(model_path, "wb") as f:
        pickle.dump(clf, f)

    print(f"[ML] Model successfully trained and saved to {model_path}")

if __name__ == "__main__":
    train_model()
