import unittest
import json
from hollarek.misc import get_salvaged_json
from hollarek.dev import log, LogLevel


# ---------------------------------------------------------
class CustomTestResult(unittest.TestResult):
    test_spaces = 50  # Space allocated for test names
    status_spaces = 20  # Space allocated for status messages

    def addSuccess(self, test):
        super().addSuccess(test)
        test_name = test.id()  # This gets the full name of the test
        log(f'{test_name:<{self.test_spaces}} {"SUCCESS":<{self.status_spaces}}', LogLevel.INFO)

    def addError(self, test, err):
        super().addError(test, err)
        test_name = test.id()  # Adjusted to use test.id()
        log(f'{test_name:<{self.test_spaces}} {"ERROR":<{self.status_spaces}}', LogLevel.CRITICAL)

    def addFailure(self, test, err):
        super().addFailure(test, err)
        test_name = test.id()  # Adjusted to use test.id()
        log(f'{test_name:<{self.test_spaces}} {"FAIL":<{self.status_spaces}}', LogLevel.ERROR)

    def addSkip(self, test, reason):
        super().addSkip(test, reason)
        test_name = test.id()  # Adjusted to use test.id()
        log(f'{test_name:<{self.test_spaces}} {"SKIPPED":<{self.status_spaces}}', LogLevel.INFO)




class Unittest(unittest.TestCase):

    def setUp(self):
        # Setting up broken json strings as attributes
        self.valid_str = '{"key": "value"}'
        self.broken_str_newline = '{"key": "value with a new\nline"}'
        self.broken_str_tab = '{"key": "value with a tab\t"}'
        self.broken_str_multiple = '{"key": "new\nline and\ttab"}'

    def run(self, result=None):
        try:
            super().run(result)  # Call the original run method, which will execute the test method.
        except Exception as e:
            self.fail(f"Test failed with error: {e}")

    def test_no_control_characters(self):
        repaired_str = get_salvaged_json(self.valid_str)
        parsed_json = json.loads(repaired_str)
        self.assertEqual(parsed_json['key'], "value")

    def test_single_newline(self):
        repaired_str = get_salvaged_json(self.broken_str_newline)
        parsed_json = json.loads(repaired_str)
        self.assertEqual(parsed_json['key'], "value with a new\nline")

    def test_tab_and_backslash(self):
        repaired_str = get_salvaged_json(self.broken_str_tab)
        parsed_json = json.loads(repaired_str)
        self.assertEqual(parsed_json['key'], "value with a tab\t")

    def test_multiple_control_characters(self):
        repaired_str = get_salvaged_json(self.broken_str_multiple)
        parsed_json = json.loads(repaired_str)
        self.assertEqual(parsed_json['key'], "new\nline and\ttab")


def test():
    suite = unittest.TestLoader().loadTestsFromTestCase(Unittest)
    # Use CustomTestResult with TextTestRunner
    runner = unittest.TextTestRunner(resultclass=CustomTestResult, verbosity=2)
    runner.run(suite)


if __name__ == "__main__":
    test()
