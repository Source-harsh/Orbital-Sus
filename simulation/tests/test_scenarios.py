from simulation.scenarios import (
    run_normal,
    run_hardware_fault,
    run_environmental_disturbance,
    run_cyber_attack
)


def test_normal():

    state = run_normal()

    assert state.command_type == "AUTHORIZED"
    assert state.communication_anomaly is False


def test_hardware_fault():

    state = run_hardware_fault()

    assert state.temperature > 70
    assert state.mission_mode == "DEGRADED"


def test_environmental_disturbance():

    state = run_environmental_disturbance()

    assert state.solar_power < 40
    assert state.mission_mode == "DISTURBED"


def test_cyber_attack():

    state = run_cyber_attack()

    assert state.command_type == "UNAUTHORIZED"
    assert state.command_frequency > 10
    assert state.communication_anomaly is True