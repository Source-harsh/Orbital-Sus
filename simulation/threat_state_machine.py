class ThreatStateMachine:

    STATES = {
        "NOMINAL",
        "ANOMALY_DETECTED",
        "UNDER_INVESTIGATION",
        "CYBER_SUSPECTED",
        "THREAT_ASSESSMENT",
        "CONTAINMENT",
        "SAFE_MODE",
        "TRUSTED_MONITORING",
        "RECOVERY"
    }

    def __init__(self):

        self.state = "NOMINAL"

        self.history = [
            {
                "state": "NOMINAL",
                "event": "SYSTEM_STARTED"
            }
        ]

    def transition(self, new_state, event):

        if new_state not in self.STATES:

            raise ValueError(
                f"Invalid state: {new_state}"
            )

        self.state = new_state

        self.history.append({
            "state": new_state,
            "event": event
        })

    def process_detection(self, correlation_result):

        classification = correlation_result[
            "classification"
        ]

        threat_level = correlation_result[
            "threat_level"
        ]

        if classification == "NORMAL":

            return self.state

        self.transition(
            "ANOMALY_DETECTED",
            "ABNORMAL_BEHAVIOUR_DETECTED"
        )

        self.transition(
            "UNDER_INVESTIGATION",
            "CORRELATING_TELEMETRY"
        )

        if classification == "CYBER_ANOMALY":

            self.transition(
                "CYBER_SUSPECTED",
                "CYBER_INDICATORS_CORRELATED"
            )

            self.transition(
                "THREAT_ASSESSMENT",
                f"THREAT_LEVEL_{threat_level}"
            )

            if threat_level in {
                "HIGH",
                "CRITICAL"
            }:

                self.transition(
                    "CONTAINMENT",
                    "AUTOMATED_CONTAINMENT_TRIGGERED"
                )

        else:

            self.transition(
                "RECOVERY",
                f"NON_CYBER_EVENT_{classification}"
            )

        return self.state

    def enter_safe_mode(self):

        self.transition(
            "SAFE_MODE",
            "SAFE_MODE_ACTIVATED"
        )

    def start_monitoring(self):

        self.transition(
            "TRUSTED_MONITORING",
            "TRUSTED_TELEMETRY_MONITORING"
        )

    def recover(self):

        self.transition(
            "RECOVERY",
            "RECOVERY_STARTED"
        )

        self.transition(
            "NOMINAL",
            "SYSTEM_RETURNED_TO_NOMINAL"
        )

    def get_history(self):

        return list(self.history)