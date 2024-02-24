from hollarek.dev import get_logger, LogSettings, LogLevel

class Loggable:
    def __init__(self, settings : LogSettings = LogSettings()):
        self.logger = get_logger(settings)

    def log(self,msg : str, level : LogLevel = LogLevel.INFO):
        self.logger.log(msg=msg, level=level)

