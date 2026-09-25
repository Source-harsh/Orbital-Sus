from datetime import datetime, timezone


class ReplayLogger:

    def __init__(self):

        self.events = []

    def log(self, event, details=None):

        record = {
            "sequence": len(self.events),

            "timestamp":
                datetime.now(timezone.utc).isoformat(),

            "event": event,

            "details": details or {}
        }

        self.events.append(record)

        return record

    def get_events(self):

        return list(self.events)

    def clear(self):

        self.events.clear()

    def print_timeline(self):

        print("\n=== ORBITAL SUS EVENT TIMELINE ===\n")

        for event in self.events:

            print(
                f"T+{event['sequence']:02d} | "
                f"{event['event']} | "
                f"{event['details']}"
            )