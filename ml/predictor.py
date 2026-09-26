import os
import pickle
import math
import numpy as np
from typing import Dict, Any, Tuple

MODEL_PATH = os.path.join(os.path.dirname(__file__), "spacecraft_ml_model.pkl")

class TelemetryPredictor:
    def __init__(self):
        self.model = None
        self.load_model()

    def load_model(self):
        if os.path.exists(MODEL_PATH):
            try:
                with open(MODEL_PATH, "rb") as f:
                    self.model = pickle.load(f)
                print(f"[ML Predictor] Loaded model from {MODEL_PATH}")
            except Exception as e:
                print(f"[ML Predictor] Failed to load model: {e}")

    def predict(self, telemetry_dict: Dict[str, Any]) -> Tuple[str, float]:
        """
        Extract feature vector and return predicted classification name and anomaly score.
        """
        # Feature extraction matching dataset schema
        cmd_type_code = 0
        if telemetry_dict.get("command_type") == "UNAUTHORIZED":
            cmd_type_code = 1
        elif telemetry_dict.get("command_type") == "SPOOFED":
            cmd_type_code = 2

        gyro_mag = math.sqrt(
            telemetry_dict.get("gyro_x", 0.0)**2 +
            telemetry_dict.get("gyro_y", 0.0)**2 +
            telemetry_dict.get("gyro_z", 0.0)**2
        )

        features = [
            telemetry_dict.get("temperature", 25.0),
            telemetry_dict.get("battery", 90.0),
            telemetry_dict.get("solar_power", 75.0),
            gyro_mag,
            telemetry_dict.get("attitude", 0.0),
            telemetry_dict.get("cpu_usage", 30.0),
            cmd_type_code,
            telemetry_dict.get("command_frequency", 1),
            1 if telemetry_dict.get("communication_anomaly") else 0
        ]

        if self.model:
            try:
                prediction = self.model.predict([features])[0]
                probs = self.model.predict_proba([features])[0]
                classes = list(self.model.classes_)
                
                # Anomaly score is 1 - prob(NORMAL)
                normal_idx = classes.index("NORMAL") if "NORMAL" in classes else -1
                anomaly_score = 1.0 - probs[normal_idx] if normal_idx != -1 else 0.8
                return prediction, round(anomaly_score, 3)
            except Exception as e:
                print(f"[ML Predictor] Model prediction error: {e}")

        # Heuristic fallback if model pickle not loaded
        if cmd_type_code > 0 or telemetry_dict.get("communication_anomaly") or telemetry_dict.get("command_frequency", 1) > 8:
            return "CYBER_ANOMALY", 0.88
        elif telemetry_dict.get("battery", 90) < 25 or telemetry_dict.get("temperature", 25) > 75:
            return "HARDWARE_FAULT", 0.75
        elif telemetry_dict.get("attitude", 0) > 1.0 or telemetry_dict.get("solar_power", 75) < 30:
            return "ENVIRONMENTAL_DISTURBANCE", 0.50

        return "NORMAL", 0.05
