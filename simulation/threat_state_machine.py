class ThreatStateMachine:

    STATES = [
        "NOMINAL",
        "ANOMALY_DETECTED",
        "UNDER_INVESTIGATION",
        "CYBER_SUSPECTED",
        "THREAT_ASSESSMENT",
        "CONTAINMENT",
        "SAFE_MODE",
        "TRUSTED_MONITORING",
        "RECOVERY"
    ]

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

        self.history.append(
            {
                "state": new_state,
                "event": event
            }
        )

        return self.state

    def process_detection(self, correlation_result):

        classification = correlation_result["classification"]
        threat_level = correlation_result["threat_level"]

        # --------------------------------
        # Step 1: anomaly detected
        # --------------------------------

        if classification != "NORMAL":

            self.transition(
                "ANOMALY_DETECTED",
                "ABNORMAL_BEHAVIOUR_DETECTED"
            )

        # --------------------------------
        # Step 2: investigation
        # --------------------------------

        self.transition(
            "UNDER_INVESTIGATION",
            "CORRELATING_TELEMETRY"
        )

        # --------------------------------
        # Step 3: cyber suspicion
        # --------------------------------

        if classification == "CYBER_ANOMALY":

            self.transition(
                "CYBER_SUSPECTED",
                "CYBER_INDICATORS_CORRELATED"
            )

            self.transition(
                "THREAT_ASSESSMENT",
                f"THREAT_LEVEL_{threat_level}"
            )

            if threat_level in ["HIGH", "CRITICAL"]:

                self.transition(
                    "CONTAINMENT",
                    "AUTOMATED_CONTAINMENT_TRIGGERED"
                )

        else:

            # Hardware/environmental anomaly
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

        return self.history


if __name__ == "__main__":

    machine = ThreatStateMachine()

    correlation_result = {
        "classification": "CYBER_ANOMALY",
        "threat_level": "CRITICAL"
    }

    machine.process_detection(correlation_result)

    machine.enter_safe_mode()
    machine.start_monitoring()
    machine.recover()

    print("Final state:", machine.state)

    print("\nState history:")

    for event in machine.get_history():

        print(event)