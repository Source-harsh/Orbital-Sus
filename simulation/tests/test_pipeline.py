from simulation.simulation_runner import (
    run_scenario
)


def test_normal_pipeline():

    result = run_scenario(
        "NORMAL",
        {
            "anomaly": False,
            "anomaly_score": 0.05
        }
    )

    assert (
        result["threat"]["classification"]
        == "NORMAL"
    )

    assert (
        result["response"]["command_blocked"]
        is False
    )


def test_hardware_fault_pipeline():

    result = run_scenario(
        "HARDWARE_FAULT",
        {
            "anomaly": True,
            "anomaly_score": 0.86
        }
    )

    assert (
        result["threat"]["classification"]
        == "HARDWARE_FAULT"
    )

    assert (
        result["response"]["command_blocked"]
        is False
    )

    assert (
        result["response"]["channel_isolated"]
        is False
    )


def test_environmental_pipeline():

    result = run_scenario(
        "ENVIRONMENTAL_DISTURBANCE",
        {
            "anomaly": True,
            "anomaly_score": 0.72
        }
    )

    assert (
        result["threat"]["classification"]
        == "ENVIRONMENTAL_DISTURBANCE"
    )

    assert (
        result["response"]["command_blocked"]
        is False
    )


def test_cyber_pipeline():

    result = run_scenario(
        "CYBER_ATTACK",
        {
            "anomaly": True,
            "anomaly_score": 0.91,
            "classification": "CYBER_ANOMALY",
            "confidence": 0.94
        }
    )

    assert (
        result["threat"]["classification"]
        == "CYBER_ANOMALY"
    )

    assert (
        result["threat"]["level"]
        in {"HIGH", "CRITICAL"}
    )

    assert (
        result["response"]["command_blocked"]
        is True
    )

    assert (
        result["response"]["channel_isolated"]
        is True
    )

    assert (
        result["response"]["monitoring"]
        is True
    )

    assert (
        result["response"]["recovery"]
        is True
    )

    assert (
        result["state"]["current"]
        == "NOMINAL"
    )


def test_invalid_scenario():

    try:

        run_scenario("INVALID_SCENARIO")

        assert False

    except ValueError:

        assert True