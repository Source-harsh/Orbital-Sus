import argparse

from .scenarios import (
    run_normal,
    run_hardware_fault,
    run_environmental_disturbance,
    run_cyber_attack
)

from .correlation import correlate_threat
from .threat_state_machine import ThreatStateMachine
from .response_engine import ResponseEngine
from .replay import ReplayLogger


VALID_SCENARIOS = {
    "NORMAL",
    "HARDWARE_FAULT",
    "ENVIRONMENTAL_DISTURBANCE",
    "CYBER_ATTACK"
}


def get_scenario_state(scenario):

    scenario_functions = {
        "NORMAL": run_normal,
        "HARDWARE_FAULT": run_hardware_fault,
        "ENVIRONMENTAL_DISTURBANCE":
            run_environmental_disturbance,
        "CYBER_ATTACK": run_cyber_attack
    }

    if scenario not in scenario_functions:

        raise ValueError(
            f"Invalid scenario '{scenario}'. "
            f"Valid scenarios: "
            f"{sorted(VALID_SCENARIOS)}"
        )

    return scenario_functions[scenario]()


def default_ml_result(scenario):

    if scenario == "NORMAL":

        return {
            "anomaly": False,
            "anomaly_score": 0.05,
            "classification": "NORMAL",
            "confidence": 0.98
        }

    if scenario == "CYBER_ATTACK":

        return {
            "anomaly": True,
            "anomaly_score": 0.91,
            "classification": "CYBER_ANOMALY",
            "confidence": 0.94
        }

    if scenario == "HARDWARE_FAULT":

        return {
            "anomaly": True,
            "anomaly_score": 0.86,
            "classification": "HARDWARE_FAULT",
            "confidence": 0.91
        }

    return {
        "anomaly": True,
        "anomaly_score": 0.72,
        "classification":
            "ENVIRONMENTAL_DISTURBANCE",
        "confidence": 0.87
    }


def run_scenario(
    scenario,
    ml_result=None,
    perform_recovery=True
):
    """
    Main public API for the simulation module.

    Parameters
    ----------
    scenario:
        NORMAL
        HARDWARE_FAULT
        ENVIRONMENTAL_DISTURBANCE
        CYBER_ATTACK

    ml_result:
        Output received from the ML module.

    perform_recovery:
        Whether the controlled simulation should
        demonstrate recovery after containment.
    """

    if scenario not in VALID_SCENARIOS:

        raise ValueError(
            f"Invalid scenario: {scenario}"
        )

    if ml_result is None:

        ml_result = default_ml_result(
            scenario
        )

    satellite = get_scenario_state(
        scenario
    )

    replay = ReplayLogger()

    replay.log(
        "SCENARIO_STARTED",
        {
            "scenario": scenario,
            "satellite_id":
                satellite.satellite_id
        }
    )

    replay.log(
        "TELEMETRY_GENERATED",
        satellite.to_dict()
    )

    # -----------------------------
    # Threat correlation
    # -----------------------------

    threat = correlate_threat(
        satellite,
        ml_result
    )

    replay.log(
        "THREAT_CORRELATED",
        threat
    )

    # -----------------------------
    # Threat state machine
    # -----------------------------

    state_machine = ThreatStateMachine()

    state_machine.process_detection(
        threat
    )

    # -----------------------------
    # Response engine
    # -----------------------------

    response_engine = ResponseEngine()

    containment_triggered = (
        threat["classification"]
        == "CYBER_ANOMALY"
        and threat["threat_level"]
        in {"HIGH", "CRITICAL"}
    )

    if containment_triggered:

        replay.log(
            "CYBER_THREAT_CONFIRMED",
            {
                "threat_level":
                    threat["threat_level"]
            }
        )

        state_machine.enter_safe_mode()

        containment = (
            response_engine
            .execute_containment()
        )

        replay.log(
            "CONTAINMENT_EXECUTED",
            containment
        )

        state_machine.start_monitoring()

        replay.log(
            "TRUSTED_MONITORING_STARTED"
        )

        # -----------------------------
        # Controlled recovery
        # -----------------------------

        if perform_recovery:

            replay.log(
                "TELEMETRY_STABLE",
                {
                    "recovery_condition":
                        "SIMULATED_STABILITY_CONFIRMED"
                }
            )

            recovery = (
                response_engine
                .execute_recovery()
            )

            state_machine.recover()

            replay.log(
                "RECOVERY_COMPLETED",
                recovery
            )

    else:

        replay.log(
            "NO_CYBER_CONTAINMENT",
            {
                "classification":
                    threat["classification"]
            }
        )

        recovery = None

    response_status = (
        response_engine.get_status()
    )

    return {
        "satellite_id":
            satellite.satellite_id,

        "scenario":
            scenario,

        "telemetry":
            satellite.to_dict(),

        "ml_result":
            ml_result,

        "threat": {
            "score":
                threat["threat_score"],

            "level":
                threat["threat_level"],

            "classification":
                threat["classification"],

            "evidence":
                threat["evidence"]
        },

        "response":
            response_status,

        "state": {
            "current":
                state_machine.state,

            "history":
                state_machine.get_history()
        },

        "events":
            replay.get_events()
    }


def print_summary(result):

    print("\n========================================")
    print("         ORBITAL SUS SIMULATION")
    print("========================================")

    print(
        f"\nScenario: "
        f"{result['scenario']}"
    )

    print(
        f"Classification: "
        f"{result['threat']['classification']}"
    )

    print(
        f"Threat Level: "
        f"{result['threat']['level']}"
    )

    print(
        f"Threat Score: "
        f"{result['threat']['score']}"
    )

    print("\nResponse:")

    response = result["response"]

    print(
        f"  Command Blocked : "
        f"{response['command_blocked']}"
    )

    print(
        f"  Channel Isolated: "
        f"{response['channel_isolated']}"
    )

    print(
        f"  Safe Mode       : "
        f"{response['safe_mode']}"
    )

    print(
        f"  Monitoring      : "
        f"{response['monitoring']}"
    )

    print(
        f"  Recovery        : "
        f"{response['recovery']}"
    )

    print(
        f"\nFinal State: "
        f"{result['state']['current']}"
    )

    print("\nEvent Timeline:")

    for event in result["events"]:

        print(
            f"  T+{event['sequence']:02d} "
            f"{event['event']}"
        )

    print("\n========================================")


def main():

    parser = argparse.ArgumentParser(
        description=
        "Orbital Sus spacecraft simulation"
    )

    parser.add_argument(
        "--scenario",
        required=True,
        choices=sorted(VALID_SCENARIOS),
        help="Simulation scenario"
    )

    parser.add_argument(
        "--no-recovery",
        action="store_true",
        help="Stop after containment"
    )

    args = parser.parse_args()

    result = run_scenario(
        scenario=args.scenario,
        perform_recovery=not args.no_recovery
    )

    print_summary(result)


if __name__ == "__main__":
    main()