from enum import Enum
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict

class ScenarioName(str, Enum):
    NORMAL = "NORMAL"
    HARDWARE_FAULT = "HARDWARE_FAULT"
    ENVIRONMENTAL_DISTURBANCE = "ENVIRONMENTAL_DISTURBANCE"
    CYBER_ATTACK = "CYBER_ATTACK"

class ClassificationName(str, Enum):
    NORMAL = "NORMAL"
    HARDWARE_FAULT = "HARDWARE_FAULT"
    ENVIRONMENTAL_DISTURBANCE = "ENVIRONMENTAL_DISTURBANCE"
    CYBER_ANOMALY = "CYBER_ANOMALY"

class ThreatLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class ResponseState(str, Enum):
    ALERT = "ALERT"
    INCREASE_MONITORING = "INCREASE_MONITORING"
    BLOCK_COMMAND = "BLOCK_COMMAND"
    ISOLATE_CHANNEL = "ISOLATE_CHANNEL"
    SAFE_MODE = "SAFE_MODE"
    RECOVERY = "RECOVERY"

class TelemetryData(BaseModel):
    model_config = ConfigDict(extra="ignore")

    satellite_id: str = Field(default="SAT-01", description="Identifier for target satellite")
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z", description="ISO timestamp")
    temperature: float = Field(default=24.5, description="Subsystem temperature in Celsius")
    battery: float = Field(default=95.0, description="State of charge percentage (0-100%)")
    solar_power: float = Field(default=80.0, description="Solar array power output in Watts")
    gyro_x: float = Field(default=0.0, description="Gyroscope angular rate X (rad/s)")
    gyro_y: float = Field(default=0.0, description="Gyroscope angular rate Y (rad/s)")
    gyro_z: float = Field(default=0.0, description="Gyroscope angular rate Z (rad/s)")
    attitude: float = Field(default=0.0, description="Attitude deviation in degrees")
    cpu_usage: float = Field(default=30.0, description="CPU load percentage (0-100%)")
    command_type: str = Field(default="AUTHORIZED", description="Command type (AUTHORIZED, UNAUTHORIZED, SPOOFED)")
    command_frequency: int = Field(default=1, description="Commands received per second")
    communication_anomaly: bool = Field(default=False, description="Flag indicating comms anomaly")

class AssessmentResult(BaseModel):
    satellite_id: str
    timestamp: str
    scenario: ScenarioName
    classification: ClassificationName
    threat_level: ThreatLevel
    recommended_response: ResponseState
    anomaly_score: float = Field(ge=0.0, le=1.0)
    details: str

class SystemState(BaseModel):
    satellite_id: str
    active_response: ResponseState
    threat_level: ThreatLevel
    telemetry: TelemetryData
    last_updated: str
