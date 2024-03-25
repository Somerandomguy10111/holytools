from hollarek.abstract.integer_inf import IntInf
from hollarek.devtools import Unittest

class TestIntInf(Unittest):

    def test_sign_initialization(self):
        self.assertEqual(IntInf('+').sign, '+')
        self.assertEqual(IntInf('-').sign, '-')
        with self.assertRaises(ValueError):
            IntInf('invalid')

    def test_equality(self):
        self.assertTrue(IntInf('+') == IntInf('+'))
        self.assertFalse(IntInf('+') == IntInf('-'))

    def test_inequality(self):
        self.assertTrue(IntInf('+') != IntInf('-'))
        self.assertFalse(IntInf('+') != IntInf('+'))

    def test_less_than(self):
        self.assertTrue(IntInf('-') < IntInf('+'))
        self.assertFalse(IntInf('+') < IntInf('-'))
        self.assertTrue(IntInf('-') < 10)  # Negative infinity less than any real int
        self.assertFalse(IntInf('+') < 10)  # Positive infinity not less than any real int

    def test_less_than_or_equal(self):
        self.assertTrue(IntInf('-') <= IntInf('+'))
        self.assertTrue(IntInf('-') <= IntInf('-'))
        self.assertTrue(IntInf('-') <= 10)  # Negative infinity less than any real int
        self.assertFalse(IntInf('+') <= 10)  # Positive infinity not less than any real int

    def test_greater_than(self):
        self.assertTrue(IntInf('+') > IntInf('-'))
        self.assertFalse(IntInf('-') > IntInf('+'))
        self.assertTrue(IntInf('+') > 10)  # Positive infinity greater than any real int
        self.assertFalse(IntInf('-') > 10)  # Negative infinity not greater than any real int

    def test_greater_than_or_equal(self):
        self.assertTrue(IntInf('+') >= IntInf('-'))
        self.assertTrue(IntInf('+') >= IntInf('+'))
        self.assertTrue(IntInf('+') >= 10)  # Positive infinity greater than any real int
        self.assertFalse(IntInf('-') >= 10)  # Negative infinity not greater than any real int

    def test_addition(self):
        with self.assertRaises(ValueError):
            IntInf('+') + IntInf('-')

    def test_subtraction(self):
        with self.assertRaises(ValueError):
            IntInf('+') - IntInf('-')

    def test_not_implemented_operations(self):
        with self.assertRaises(NotImplementedError):
            IntInf('+') * 2
        with self.assertRaises(NotImplementedError):
            IntInf('+') / 2
        with self.assertRaises(NotImplementedError):
            IntInf('+') ** 2

if __name__ == "__main__":
    TestIntInf.execute_all()