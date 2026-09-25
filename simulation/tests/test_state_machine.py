from simulation.threat_state_machine import (
    ThreatStateMachine
)


def test_cyber_state_flow():

    machine = ThreatStateMachine()

    result = machine.process_detection({
        "classification": "CYBER_ANOMALY",
        "threat_level": "CRITICAL"
    })

    assert result == "CONTAINMENT"

    machine.enter_safe_mode()

    assert machine.state == "SAFE_MODE"

    machine.start_monitoring()

    assert machine.state == "TRUSTED_MONITORING"

    machine.recover()

    assert machine.state == "NOMINAL"


def test_normal_stays_nominal():

    machine = ThreatStateMachine()

    result = machine.process_detection({
        "classification": "NORMAL",
        "threat_level": "LOW"
    })

    assert result == "NOMINAL"