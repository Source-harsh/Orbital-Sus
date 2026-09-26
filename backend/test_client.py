import requests
import json
import time

BASE_URL = "http://127.0.0.1:8000"

telemetry_samples = [
    {
        "name": "Normal Operation",
        "data": {
            "satellite_id": "SAT-01",
            "temperature": 24.5,
            "battery": 92.0,
            "solar_power": 78.5,
            "gyro_x": 0.01,
            "gyro_y": 0.02,
            "gyro_z": 0.01,
            "attitude": 0.02,
            "cpu_usage": 28.5,
            "command_type": "AUTHORIZED",
            "command_frequency": 1,
            "communication_anomaly": False
        }
    },
    {
        "name": "Cyber Attack - Command Injection & Comms Anomaly",
        "data": {
            "satellite_id": "SAT-01",
            "temperature": 32.1,
            "battery": 88.0,
            "solar_power": 75.0,
            "gyro_x": 0.15,
            "gyro_y": 0.08,
            "gyro_z": 0.12,
            "attitude": 3.40,
            "cpu_usage": 94.2,
            "command_type": "UNAUTHORIZED",
            "command_frequency": 15,
            "communication_anomaly": True
        }
    },
    {
        "name": "Hardware Fault - Battery & Thermal Spike",
        "data": {
            "satellite_id": "SAT-01",
            "temperature": 82.5,
            "battery": 14.2,
            "solar_power": 45.0,
            "gyro_x": 0.02,
            "gyro_y": 0.01,
            "gyro_z": 0.03,
            "attitude": 18.2,
            "cpu_usage": 45.0,
            "command_type": "AUTHORIZED",
            "command_frequency": 2,
            "communication_anomaly": False
        }
    }
]

def test_telemetry():
    print("--- Testing Spacecraft Cyber Defense Backend ---")
    for sample in telemetry_samples:
        print(f"\n[Sending Payload]: {sample['name']}")
        try:
            res = requests.post(f"{BASE_URL}/api/telemetry", json=sample['data'])
            if res.status_code == 200:
                result = res.json()
                print(" -> Scenario:", result["scenario"])
                print(" -> Classification:", result["classification"])
                print(" -> Threat Level:", result["threat_level"])
                print(" -> Recommended Response:", result["recommended_response"])
                print(" -> Anomaly Score:", result["anomaly_score"])
                print(" -> Details:", result["details"])
            else:
                print("Error:", res.status_code, res.text)
        except Exception as e:
            print("Failed to connect to backend server. Make sure FastAPI server is running (`uvicorn main:app --reload`).")
            print("Error detail:", e)
            break
        time.sleep(1)

if __name__ == "__main__":
    test_telemetry()
