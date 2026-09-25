from simulator import create_normal_state


def unauthorized_command_attack():

    state = create_normal_state()

    state.command_type = "UNAUTHORIZED"
    state.command_frequency = 15

    state.communication_anomaly = True

    state.attitude = 8.5
    state.cpu_usage = 92.0

    state.security_state = "SUSPICIOUS"

    return state


def command_flood_attack():

    state = create_normal_state()

    state.command_type = "UNAUTHORIZED"
    state.command_frequency = 30

    state.communication_anomaly = True
    state.cpu_usage = 95.0

    state.security_state = "SUSPICIOUS"

    return state


def communication_intrusion():

    state = create_normal_state()

    state.command_type = "AUTHORIZED"
    state.command_frequency = 2

    state.communication_anomaly = True

    state.cpu_usage = 75.0

    state.security_state = "SUSPICIOUS"

    return state


def run_attack(attack_type="UNAUTHORIZED_COMMAND"):

    if attack_type == "UNAUTHORIZED_COMMAND":
        return unauthorized_command_attack()

    if attack_type == "COMMAND_FLOOD":
        return command_flood_attack()

    if attack_type == "COMMUNICATION_INTRUSION":
        return communication_intrusion()

    raise ValueError(f"Unknown attack type: {attack_type}")


if __name__ == "__main__":

    attack = run_attack()

    print("=== Cyber Attack Simulation ===")
    print(attack.to_dict())