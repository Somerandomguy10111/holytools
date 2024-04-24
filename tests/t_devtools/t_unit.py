from hollarek.devtools import Unittest
from tests.t_devtools.t_dtyping import TestOptionalTyping


class TestMeta(Unittest):
    def test_summary(self):
        results = TestOptionalTyping.execute_all()
        self.assertIn(f'tests ran successfully!',results.get_final_status())

    def test_error(self):
        raise ValueError(f'This bug is tamed and very friendly')

    def test_fail(self):
        self.fail(msg=f'I failed this test on purposes')


if __name__ == "__main__":
    TestMeta.execute_all()