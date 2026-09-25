from .simulator import create_normal_state


def simulate_temperature_fault():

    state = create_normal_state()

    state.temperature = 85.0
    state.mission_mode = "DEGRADED"

    return state


def simulate_gyro_fault():

    state = create_normal_state()

    state.gyro_x = 4.5
    state.gyro_y = 3.2
    state.gyro_z = 2.8

    state.attitude = 5.0
    state.mission_mode = "DEGRADED"

    return state


def simulate_power_fault():

    state = create_normal_state()

    state.battery = 25.0
    state.solar_power = 15.0

    state.mission_mode = "DEGRADED"

    return state


def simulate_environmental_disturbance():

    state = create_normal_state()

    state.temperature = 45.0
    state.solar_power = 25.0
    state.attitude = 4.0

    state.mission_mode = "DISTURBED"

    return state


if __name__ == "__main__":

    print("=== Temperature Fault ===")
    print(simulate_temperature_fault().to_dict())

    print("\n=== Gyro Fault ===")
    print(simulate_gyro_fault().to_dict())

    print("\n=== Power Fault ===")
    print(simulate_power_fault().to_dict())

    print("\n=== Environmental Disturbance ===")
    print(simulate_environmental_disturbance().to_dict())