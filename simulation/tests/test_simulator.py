from simulation.simulator import (
    create_normal_state
)


def test_normal_state():

    state = create_normal_state()

    assert state.satellite_id == "SAT-01"
    assert state.temperature == 24.5
    assert state.battery == 87.0
    assert state.command_type == "AUTHORIZED"
    assert state.communication_anomaly is False
    assert state.mission_mode == "NOMINAL"