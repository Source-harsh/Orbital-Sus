import json
from pathlib import Path


CONFIG_PATH = Path(__file__).with_name(
    "scenario_config.json"
)


def load_config():

    with open(CONFIG_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def calculate_threat_level(score, config):

    levels = config["threat_levels"]

    if score >= levels["CRITICAL"]["minimum_score"]:
        return "CRITICAL"

    if score >= levels["HIGH"]["minimum_score"]:
        return "HIGH"

    if score >= levels["MEDIUM"]["minimum_score"]:
        return "MEDIUM"

    return "LOW"


def correlate_threat(state, ml_result):

    config = load_config()

    thresholds = config["thresholds"]
    weights = config["threat_scoring"]

    score = 0
    evidence = []

    # -------------------------
    # ML anomaly
    # -------------------------

    if ml_result.get("anomaly", False):

        score += weights["ml_anomaly"]

        evidence.append({
            "indicator": "ML_ANOMALY",
            "weight": weights["ml_anomaly"],
            "value": ml_result.get("anomaly_score")
        })

    # -------------------------
    # Unauthorized command
    # -------------------------

    if state.command_type == "UNAUTHORIZED":

        score += weights["unauthorized_command"]

        evidence.append({
            "indicator": "UNAUTHORIZED_COMMAND",
            "weight": weights["unauthorized_command"],
            "value": state.command_type
        })

    # -------------------------
    # Communication anomaly
    # -------------------------

    if state.communication_anomaly:

        score += weights["communication_anomaly"]

        evidence.append({
            "indicator": "COMMUNICATION_ANOMALY",
            "weight": weights["communication_anomaly"],
            "value": True
        })

    # -------------------------
    # Attitude deviation
    # -------------------------

    if abs(state.attitude) > thresholds["attitude_deviation"]:

        score += weights["attitude_deviation"]

        evidence.append({
            "indicator": "ATTITUDE_DEVIATION",
            "weight": weights["attitude_deviation"],
            "value": state.attitude
        })

    # -------------------------
    # Abnormal command rate
    # -------------------------

    if (
        state.command_frequency
        > thresholds["command_frequency_high"]
    ):

        score += weights["abnormal_command_rate"]

        evidence.append({
            "indicator": "ABNORMAL_COMMAND_RATE",
            "weight": weights["abnormal_command_rate"],
            "value": state.command_frequency
        })

    # -------------------------
    # Threat level
    # -------------------------

    threat_level = calculate_threat_level(
        score,
        config
    )

    # -------------------------
    # Classification
    # -------------------------

    cyber_indicators = (
        state.command_type == "UNAUTHORIZED"
        and state.communication_anomaly
    )

    hardware_indicators = (
        state.temperature
        > thresholds["temperature_high"]
        or abs(state.gyro_x)
        > thresholds["gyro_deviation"]
        or state.battery
        < thresholds["battery_low"]
    )

    environmental_indicators = (
        state.solar_power
        < thresholds["solar_power_low"]
        or (
            state.temperature
            > thresholds["temperature_environmental"]
            and state.temperature
            <= thresholds["temperature_high"]
        )
        or (
            abs(state.attitude)
            > thresholds["attitude_environmental"]
            and not cyber_indicators
        )
    )

    if cyber_indicators and score >= 4:

        classification = "CYBER_ANOMALY"

    elif hardware_indicators:

        classification = "HARDWARE_FAULT"

    elif environmental_indicators:

        classification = "ENVIRONMENTAL_DISTURBANCE"

    elif not ml_result.get("anomaly", False):

        classification = "NORMAL"

    else:

        classification = "UNKNOWN_ANOMALY"

    return {
        "threat_score": score,
        "threat_level": threat_level,
        "classification": classification,
        "evidence": evidence
    }


if __name__ == "__main__":

    from .simulator import create_normal_state

    state = create_normal_state()

    ml_result = {
        "anomaly": True,
        "anomaly_score": 0.91,
        "classification": "CYBER_ANOMALY",
        "confidence": 0.94
    }

    result = correlate_threat(
        state,
        ml_result
    )

    print(result)