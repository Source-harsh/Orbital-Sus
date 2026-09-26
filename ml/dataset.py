import pandas as pd
import numpy as np
import random

def generate_telemetry_dataset(num_samples: int = 2000, output_path: str = "telemetry_dataset.csv"):
    """Generate a realistic dataset for spacecraft cyber-physical anomaly detection."""
    data = []
    labels = []

    for _ in range(num_samples):
        # Pick scenario
        scenario = random.choices(
            ["NORMAL", "CYBER_ANOMALY", "HARDWARE_FAULT", "ENVIRONMENTAL_DISTURBANCE"],
            weights=[0.60, 0.20, 0.10, 0.10]
        )[0]

        if scenario == "NORMAL":
            temp = random.uniform(18.0, 30.0)
            battery = random.uniform(70.0, 100.0)
            solar = random.uniform(65.0, 85.0)
            gyro = random.uniform(0.001, 0.03)
            attitude = random.uniform(0.001, 0.10)
            cpu = random.uniform(15.0, 45.0)
            cmd_type = 0  # AUTHORIZED
            cmd_freq = random.randint(1, 3)
            comm_anomaly = 0

        elif scenario == "CYBER_ANOMALY":
            temp = random.uniform(30.0, 45.0)
            battery = random.uniform(40.0, 85.0)
            solar = random.uniform(50.0, 75.0)
            gyro = random.uniform(0.1, 0.6)
            attitude = random.uniform(2.0, 10.0)
            cpu = random.uniform(80.0, 100.0)
            cmd_type = random.choice([1, 2])  # 1: UNAUTHORIZED, 2: SPOOFED
            cmd_freq = random.randint(10, 30)
            comm_anomaly = random.choice([0, 1])

        elif scenario == "HARDWARE_FAULT":
            temp = random.uniform(70.0, 100.0)
            battery = random.uniform(0.0, 30.0)
            solar = random.uniform(0.0, 40.0)
            gyro = random.uniform(0.1, 0.4)
            attitude = random.uniform(10.0, 30.0)
            cpu = random.uniform(40.0, 70.0)
            cmd_type = 0
            cmd_freq = random.randint(1, 4)
            comm_anomaly = 0

        else:  # ENVIRONMENTAL_DISTURBANCE
            temp = random.uniform(25.0, 38.0)
            battery = random.uniform(50.0, 80.0)
            solar = random.uniform(10.0, 45.0)
            gyro = random.uniform(0.05, 0.20)
            attitude = random.uniform(0.5, 2.5)
            cpu = random.uniform(30.0, 60.0)
            cmd_type = 0
            cmd_freq = random.randint(1, 3)
            comm_anomaly = 0

        features = [temp, battery, solar, gyro, attitude, cpu, cmd_type, cmd_freq, comm_anomaly]
        data.append(features)
        labels.append(scenario)

    columns = [
        "temperature", "battery", "solar_power", "gyro_magnitude", 
        "attitude", "cpu_usage", "command_type_code", "command_frequency", "communication_anomaly"
    ]

    df = pd.DataFrame(data, columns=columns)
    df["label"] = labels
    df.to_csv(output_path, index=False)
    print(f"[ML] Generated dataset with {num_samples} samples at {output_path}")
    return df

if __name__ == "__main__":
    generate_telemetry_dataset()
