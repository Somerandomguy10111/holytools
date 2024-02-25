import json
from json_repair import repair_json
from hollarek.dev import Unittest


class JsonTester(Unittest):
    @classmethod
    def setUpClass(cls):
        cls.valid_str = '{"key": "value"}'
        cls.broken_str_newline = '{"key": "value with a new\nline"}'
        cls.broken_str_tab = '{"key": "value with a tab\t"}'
        cls.broken_str_multiple = '{"key": "new\nline and\ttab"}'

    def run(self, result=None):
        try:
            super().run(result)
        except Exception as e:
            self.fail(f"Test failed with error: {e}")

    def test_no_control_characters(self):
        repaired_str = repair_json(self.valid_str)
        parsed_json = json.loads(repaired_str)
        self.assertEqual(parsed_json['key'], "value")

    def test_single_newline(self):
        repaired_str = repair_json(self.broken_str_newline)
        parsed_json = json.loads(repaired_str)
        self.assertEqual(parsed_json['key'], "value with a new\nline")

    def test_tab_and_backslash(self):
        repaired_str = repair_json(self.broken_str_tab)
        parsed_json = json.loads(repaired_str)
        self.assertEqual(parsed_json['key'], "value with a tab\t")

    def test_multiple_control_characters(self):
        repaired_str = repair_json(self.broken_str_multiple)
        parsed_json = json.loads(repaired_str)
        self.assertEqual(parsed_json['keyy'], "new\nline and\ttab")



if __name__ == "__main__":
    JsonTester.execute_all(show_run_times=True)