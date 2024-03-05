import unittest
from hollarek.logging import Logger
from .result import Result
from .settings import TestSettings
# ---------------------------------------------------------


class Runner(unittest.TextTestRunner):
    def __init__(self, logger : Logger, settings : TestSettings):
        super().__init__(resultclass=None)
        self.logger : Logger = logger
        self.test_settings : TestSettings = settings

    def run(self, test) -> Result:
        result = Result(logger=self.logger,
                        stream=self.stream,
                        settings=self.test_settings,
                        descriptions=self.descriptions,
                        verbosity=2)
        test(result)
        result.printErrors()

        return result