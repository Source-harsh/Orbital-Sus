class ResponseEngine:

    def __init__(self):

        self.command_blocked = False
        self.channel_isolated = False
        self.safe_mode = False
        self.monitoring = False
        self.recovery = False

        self.action_history = []

    def block_command(self):

        self.command_blocked = True

        self.action_history.append(
            "BLOCK_COMMAND"
        )

        return {
            "action": "BLOCK_COMMAND",
            "command_blocked": True
        }

    def isolate_channel(self):

        self.channel_isolated = True

        self.action_history.append(
            "ISOLATE_CHANNEL"
        )

        return {
            "action": "ISOLATE_CHANNEL",
            "channel_isolated": True
        }

    def enter_safe_mode(self):

        self.safe_mode = True

        self.action_history.append(
            "SAFE_MODE"
        )

        return {
            "action": "SAFE_MODE",
            "safe_mode": True
        }

    def start_monitoring(self):

        self.monitoring = True

        self.action_history.append(
            "TRUSTED_MONITORING"
        )

        return {
            "action": "TRUSTED_MONITORING",
            "monitoring": True
        }

    def start_recovery(self):

        self.recovery = True

        self.safe_mode = False

        self.action_history.append(
            "RECOVERY"
        )

        return {
            "action": "RECOVERY",
            "recovery": True,
            "safe_mode": False
        }

    def execute_containment(self):

        """
        Executes the complete containment sequence.
        """

        results = []

        results.append(
            self.block_command()
        )

        results.append(
            self.isolate_channel()
        )

        results.append(
            self.enter_safe_mode()
        )

        results.append(
            self.start_monitoring()
        )

        return {
            "status": "CONTAINED",
            "actions": results,
            "command_blocked": self.command_blocked,
            "channel_isolated": self.channel_isolated,
            "safe_mode": self.safe_mode,
            "monitoring": self.monitoring,
            "recovery": self.recovery
        }

    def execute_recovery(self):

        result = self.start_recovery()

        return {
            "status": "RECOVERING",
            "command_blocked": self.command_blocked,
            "channel_isolated": self.channel_isolated,
            "safe_mode": self.safe_mode,
            "monitoring": self.monitoring,
            "recovery": self.recovery,
            "action": result
        }

    def get_status(self):

        return {
            "command_blocked": self.command_blocked,
            "channel_isolated": self.channel_isolated,
            "safe_mode": self.safe_mode,
            "monitoring": self.monitoring,
            "recovery": self.recovery
        }

    def get_action_history(self):

        return self.action_history


if __name__ == "__main__":

    engine = ResponseEngine()

    print("=== CONTAINMENT ===")

    result = engine.execute_containment()

    print(result)

    print("\n=== RECOVERY ===")

    recovery = engine.execute_recovery()

    print(recovery)