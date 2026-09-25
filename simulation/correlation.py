def correlate_threat(state, ml_result):
    """
    Combines ML output with spacecraft/cyber indicators.

    ML anomaly alone does NOT mean cyber attack.
    """

    score = 0
    evidence = []

    # -------------------------
    # ML anomaly
    # -------------------------

    if ml_result.get("anomaly", False):

        score += 1

        evidence.append({
            "indicator": "ML_ANOMALY",
            "weight": 1
        })

    # -------------------------
    # Unauthorized command
    # -------------------------

    if state.command_type == "UNAUTHORIZED":

        score += 2

        evidence.append({
            "indicator": "UNAUTHORIZED_COMMAND",
            "weight": 2
        })

    # -------------------------
    # Communication anomaly
    # -------------------------

    if state.communication_anomaly:

        score += 2

        evidence.append({
            "indicator": "COMMUNICATION_ANOMALY",
            "weight": 2
        })

    # -------------------------
    # Attitude deviation
    # -------------------------

    if abs(state.attitude) > 5:

        score += 2

        evidence.append({
            "indicator": "ATTITUDE_DEVIATION",
            "weight": 2
        })

    # -------------------------
    # Abnormal command rate
    # -------------------------

    if state.command_frequency > 10:

        score += 1

        evidence.append({
            "indicator": "ABNORMAL_COMMAND_RATE",
            "weight": 1
        })

    # -------------------------
    # Threat level
    # -------------------------

    if score >= 6:

        threat_level = "CRITICAL"

    elif score >= 4:

        threat_level = "HIGH"

    elif score >= 2:

        threat_level = "MEDIUM"

    else:

        threat_level = "LOW"

    # -------------------------
    # Classification
    # -------------------------

    if (
        state.command_type == "UNAUTHORIZED"
        and state.communication_anomaly
        and score >= 4
    ):

        classification = "CYBER_ANOMALY"

    elif (
        state.temperature > 70
        or abs(state.gyro_x) > 2
        or state.battery < 50
    ):

        classification = "HARDWARE_FAULT"

    elif (
        state.solar_power < 40
        or state.temperature > 40
        or abs(state.attitude) > 3
    ):

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

    from simulator import create_normal_state

    state = create_normal_state()

    ml_result = {
        "anomaly": True,
        "anomaly_score": 0.91,
        "classification": "CYBER_ANOMALY",
        "confidence": 0.94
    }

    result = correlate_threat(state, ml_result)

    print(result)