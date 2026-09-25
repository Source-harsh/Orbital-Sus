from simulation.response_engine import (
    ResponseEngine
)


def test_containment():

    engine = ResponseEngine()

    result = engine.execute_containment()

    assert result["command_blocked"] is True
    assert result["channel_isolated"] is True
    assert result["safe_mode"] is True
    assert result["monitoring"] is True
    assert result["recovery"] is False


def test_recovery():

    engine = ResponseEngine()

    engine.execute_containment()

    result = engine.execute_recovery()

    assert result["recovery"] is True
    assert result["safe_mode"] is False