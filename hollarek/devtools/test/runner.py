import unittest


from hollarek.logging import Logger
from .result import UnittestResult

# ---------------------------------------------------------


class CustomTestRunner(unittest.TextTestRunner):
    def __init__(self, logger : Logger, show_run_times : bool = True, show_details : bool = True):
        super().__init__(resultclass=None)
        self.logger : Logger = logger
        self.show_run_times = show_run_times
        self.show_details : bool = show_details


    def run(self, test) -> UnittestResult:
        result = UnittestResult(logger=self.logger,
                                stream=self.stream,
                                show_run_times=self.show_run_times,
                                show_details=self.show_details,
                                descriptions=self.descriptions,
                                verbosity=2)
        test(result)
        result.printErrors()

        return result