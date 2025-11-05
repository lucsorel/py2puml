class Logger:
    def __init__(self, log_level: int):
        self.log_level = log_level


class ArgsHandler:
    def __init__(self, logger: Logger, *args: str):
        self.logger = logger
        self.args = args

    def handle_args(self):
        print(self.args)
