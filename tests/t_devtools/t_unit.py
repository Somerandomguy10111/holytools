from hollarek.devtools import Unittest
from tests.t_devtools.t_dtyping import TestOptionalTyping


class TestMeta(Unittest):
    def test_summary(self):
        results = TestOptionalTyping.execute_all()
        self.assertIn(f'tests ran successfully!',results.get_final_status())


if __name__ == "__main__":
    TestMeta.execute_all()