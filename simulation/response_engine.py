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

    def isolate_channel(self):

        self.channel_isolated = True

        self.action_history.append(
            "ISOLATE_CHANNEL"
        )

    def enter_safe_mode(self):

        self.safe_mode = True

        self.action_history.append(
            "SAFE_MODE"
        )

    def start_monitoring(self):

        self.monitoring = True

        self.action_history.append(
            "TRUSTED_MONITORING"
        )

    def start_recovery(self):

        self.recovery = True
        self.safe_mode = False

        self.action_history.append(
            "RECOVERY"
        )

    def execute_containment(self):

        self.block_command()
        self.isolate_channel()
        self.enter_safe_mode()
        self.start_monitoring()

        return self.get_status()

    def execute_recovery(self):

        self.start_recovery()

        return self.get_status()

    def get_status(self):

        return {
            "command_blocked":
                self.command_blocked,

            "channel_isolated":
                self.channel_isolated,

            "safe_mode":
                self.safe_mode,

            "monitoring":
                self.monitoring,

            "recovery":
                self.recovery,

            "actions":
                list(self.action_history)
        }

    def get_action_history(self):

        return list(self.action_history)