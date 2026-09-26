import time
import math
import random
import requests
from datetime import datetime
from typing import Dict, Any

class SpacecraftSimulator:
    def __init__(self, satellite_id: str = "SAT-01", backend_url: str = "http://127.0.0.1:8000"):
        self.satellite_id = satellite_id
        self.backend_url = backend_url
        self.current_scenario = "NORMAL"
        self.step_count = 0
        
        # Nominal telemetry baseline
        self.temperature = 25.0
        self.battery = 90.0
        self.solar_power = 75.0
        self.gyro_x = 0.01
        self.gyro_y = 0.01
        self.gyro_z = 0.01
        self.attitude = 0.02
        self.cpu_usage = 30.0
        self.command_type = "AUTHORIZED"
        self.command_frequency = 1
        self.communication_anomaly = False

    def inject_scenario(self, scenario_name: str):
        """Inject a specific operational scenario/attack into the simulator."""
        print(f"\n[SIMULATOR] >>> INJECTING SCENARIO: {scenario_name} <<<")
        self.current_scenario = scenario_name

    def step(self) -> Dict[str, Any]:
        """Advance simulation by 1 timestep and compute telemetry payload."""
        self.step_count += 1
        t = self.step_count

        if self.current_scenario == "NORMAL":
            self.temperature = 25.0 + 1.5 * math.sin(t * 0.1) + random.uniform(-0.2, 0.2)
            self.battery = max(20.0, 90.0 - (t % 50) * 0.2 + random.uniform(-0.1, 0.1))
            self.solar_power = 75.0 + 5.0 * math.cos(t * 0.1) + random.uniform(-0.5, 0.5)
            self.gyro_x = 0.01 + random.uniform(-0.005, 0.005)
            self.gyro_y = 0.01 + random.uniform(-0.005, 0.005)
            self.gyro_z = 0.01 + random.uniform(-0.005, 0.005)
            self.attitude = 0.02 + random.uniform(-0.005, 0.005)
            self.cpu_usage = 30.0 + random.uniform(-2.0, 2.0)
            self.command_type = "AUTHORIZED"
            self.command_frequency = random.randint(1, 3)
            self.communication_anomaly = False

        elif self.current_scenario == "CYBER_ATTACK":
            # Cyber Attack: Command Injection, High Frequency, Comms Spoofing
            self.temperature = 35.0 + random.uniform(0.0, 5.0)
            self.battery -= 0.5
            self.solar_power = 70.0 + random.uniform(-2.0, 2.0)
            self.gyro_x = random.uniform(0.1, 0.5)
            self.gyro_y = random.uniform(0.1, 0.5)
            self.attitude = random.uniform(3.0, 8.0)
            self.cpu_usage = random.uniform(85.0, 99.0)
            self.command_type = random.choice(["UNAUTHORIZED", "SPOOFED", "MALFORMED"])
            self.command_frequency = random.randint(12, 25)
            self.communication_anomaly = True

        elif self.current_scenario == "HARDWARE_FAULT":
            # Hardware Failure: Battery drain, thermal overload, attitude loss
            self.temperature = min(95.0, self.temperature + 2.5)
            self.battery = max(5.0, self.battery - 1.5)
            self.solar_power = max(10.0, self.solar_power - 2.0)
            self.gyro_x = random.uniform(-0.3, 0.3)
            self.gyro_y = random.uniform(-0.3, 0.3)
            self.attitude = min(25.0, self.attitude + 1.2)
            self.cpu_usage = 55.0 + random.uniform(-5.0, 5.0)
            self.command_type = "AUTHORIZED"
            self.command_frequency = 2
            self.communication_anomaly = False

        elif self.current_scenario == "ENVIRONMENTAL_DISTURBANCE":
            # Solar flare / drag
            self.temperature = 32.0 + random.uniform(-1.0, 1.0)
            self.solar_power = random.uniform(20.0, 40.0)
            self.gyro_z = random.uniform(0.05, 0.15)
            self.attitude = random.uniform(0.5, 1.8)
            self.cpu_usage = 40.0 + random.uniform(-3.0, 3.0)
            self.command_type = "AUTHORIZED"
            self.command_frequency = 1
            self.communication_anomaly = False

        payload = {
            "satellite_id": self.satellite_id,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "temperature": round(self.temperature, 2),
            "battery": round(self.battery, 2),
            "solar_power": round(self.solar_power, 2),
            "gyro_x": round(self.gyro_x, 4),
            "gyro_y": round(self.gyro_y, 4),
            "gyro_z": round(self.gyro_z, 4),
            "attitude": round(self.attitude, 3),
            "cpu_usage": round(self.cpu_usage, 2),
            "command_type": self.command_type,
            "command_frequency": self.command_frequency,
            "communication_anomaly": self.communication_anomaly
        }

        return payload

    def send_telemetry(self, payload: Dict[str, Any]):
        """Stream telemetry payload to backend API endpoint."""
        try:
            res = requests.post(f"{self.backend_url}/api/telemetry", json=payload, timeout=2.0)
            if res.status_code == 200:
                result = res.json()
                print(f"[{payload['timestamp']}] Scenario: {self.current_scenario:<22} | "
                      f"Class: {result['classification']:<20} | Threat: {result['threat_level']:<8} | "
                      f"Containment Action: {result['recommended_response']}")
            else:
                print(f"[ERROR {res.status_code}]: {res.text}")
        except Exception as e:
            print(f"[DISCONNECTED]: Could not connect to backend at {self.backend_url}")
