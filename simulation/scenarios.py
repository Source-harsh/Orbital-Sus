from simulator import create_normal_state


def run_normal():
    """
    Healthy spacecraft.
    """

    state = create_normal_state()

    return state


def run_hardware_fault():
    """
    Simulates a physical hardware failure.

    Important:
    There is no unauthorized command and no communication anomaly.
    This allows the correlation engine to distinguish
    hardware problems from cyber attacks.
    """

    state = create_normal_state()

    state.temperature = 78.0
    state.gyro_x = 2.8
    state.battery = 48.0
    state.cpu_usage = 65.0

    state.mission_mode = "DEGRADED"

    return state


def run_environmental_disturbance():
    """
    Simulates an environmental disturbance.

    Example:
    Reduced solar power and attitude disturbance.
    """

    state = create_normal_state()

    state.solar_power = 28.0
    state.temperature = 42.0
    state.attitude = 3.5

    state.mission_mode = "DISTURBED"

    return state


def run_cyber_attack():
    """
    Simulates a cyber-induced spacecraft anomaly.

    Multiple indicators are intentionally correlated:
    - unauthorized command
    - high command frequency
    - communication anomaly
    - attitude deviation
    - high CPU usage
    """

    state = create_normal_state()

    state.command_type = "UNAUTHORIZED"
    state.command_frequency = 15
    state.communication_anomaly = True

    state.attitude = 8.5
    state.cpu_usage = 92.0

    state.security_state = "SUSPICIOUS"

    return state


def run_all_scenarios():

    return {
        "NORMAL": run_normal(),
        "HARDWARE_FAULT": run_hardware_fault(),
        "ENVIRONMENTAL_DISTURBANCE": run_environmental_disturbance(),
        "CYBER_ATTACK": run_cyber_attack()
    }


if __name__ == "__main__":

    scenarios = run_all_scenarios()

    for name, state in scenarios.items():

        print("\n==============================")
        print(name)
        print("==============================")

        print(state.to_dict())