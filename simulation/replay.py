from datetime import datetime


class ReplayLogger:

    def __init__(self):

        self.events = []

    def log(self, event, details=None):

        record = {
            "timestamp": datetime.now().isoformat(),
            "event": event,
            "details": details or {}
        }

        self.events.append(record)

        return record

    def get_events(self):

        return self.events

    def clear(self):

        self.events = []

    def print_timeline(self):

        print("\n=== ORBITAL SUS EVENT TIMELINE ===\n")

        for index, event in enumerate(self.events):

            print(
                f"T+{index:02d} | "
                f"{event['event']} | "
                f"{event['details']}"
            )


if __name__ == "__main__":

    logger = ReplayLogger()

    logger.log(
        "NOMINAL",
        {"mission_mode": "NOMINAL"}
    )

    logger.log(
        "UNAUTHORIZED_COMMAND",
        {"command_frequency": 15}
    )

    logger.log(
        "ATTITUDE_DEVIATION",
        {"attitude": 8.5}
    )

    logger.log(
        "COMMUNICATION_ANOMALY"
    )

    logger.log(
        "ML_ANOMALY",
        {"anomaly_score": 0.91}
    )

    logger.log(
        "CYBER_SUSPECTED"
    )

    logger.log(
        "COMMAND_BLOCKED"
    )

    logger.log(
        "CHANNEL_ISOLATED"
    )

    logger.log(
        "SAFE_MODE"
    )

    logger.log(
        "RECOVERY"
    )

    logger.print_timeline()