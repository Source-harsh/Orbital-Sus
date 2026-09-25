from simulation.scenarios import (
    run_normal,
    run_hardware_fault,
    run_environmental_disturbance,
    run_cyber_attack
)

from simulation.correlation import (
    correlate_threat
)


def test_normal_classification():

    result = correlate_threat(
        run_normal(),
        {
            "anomaly": False,
            "anomaly_score": 0.05
        }
    )

    assert result["classification"] == "NORMAL"
    assert result["threat_level"] == "LOW"


def test_hardware_fault_not_cyber():

    result = correlate_threat(
        run_hardware_fault(),
        {
            "anomaly": True,
            "anomaly_score": 0.86
        }
    )

    assert result["classification"] == "HARDWARE_FAULT"


def test_environmental_disturbance_not_cyber():

    result = correlate_threat(
        run_environmental_disturbance(),
        {
            "anomaly": True,
            "anomaly_score": 0.72
        }
    )

    assert (
        result["classification"]
        == "ENVIRONMENTAL_DISTURBANCE"
    )


def test_cyber_attack():

    result = correlate_threat(
        run_cyber_attack(),
        {
            "anomaly": True,
            "anomaly_score": 0.91
        }
    )

    assert (
        result["classification"]
        == "CYBER_ANOMALY"
    )

    assert result["threat_level"] in {
        "HIGH",
        "CRITICAL"
    }


def test_ml_anomaly_alone_not_cyber():

    result = correlate_threat(
        run_normal(),
        {
            "anomaly": True,
            "anomaly_score": 0.91
        }
    )

    assert (
        result["classification"]
        != "CYBER_ANOMALY"
    )