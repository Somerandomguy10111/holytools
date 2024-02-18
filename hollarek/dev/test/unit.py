import unittest
import json
from hollarek.misc import get_salvaged_json

# ---------------------------------------------------------

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
    unittest.TextTestRunner(verbosity=5).run(suite)


if __name__ == "__main__":
    test()
