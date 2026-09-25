from dataclasses import dataclass, asdict


@dataclass
class SatelliteState:
    satellite_id: str

    # Physical telemetry
    temperature: float
    battery: float
    solar_power: float

    # Attitude / motion
    gyro_x: float
    gyro_y: float
    gyro_z: float
    attitude: float

    # Computing / communication
    cpu_usage: float
    command_type: str
    command_frequency: int
    communication_anomaly: bool

    # Mission / security state
    mission_mode: str
    security_state: str

    def to_dict(self):
        return asdict(self)


def create_normal_state():
    """
    Creates the baseline healthy spacecraft state.
    """

    return SatelliteState(
        satellite_id="SAT-01",

        temperature=24.5,
        battery=87.0,
        solar_power=73.0,

        gyro_x=0.02,
        gyro_y=0.01,
        gyro_z=0.03,
        attitude=0.05,

        cpu_usage=41.0,
        command_type="AUTHORIZED",
        command_frequency=2,
        communication_anomaly=False,

        mission_mode="NOMINAL",
        security_state="NOMINAL"
    )


if __name__ == "__main__":
    state = create_normal_state()

    print("=== Orbital Sus Satellite Simulator ===")
    print("Normal satellite state:")
    print(state.to_dict())
