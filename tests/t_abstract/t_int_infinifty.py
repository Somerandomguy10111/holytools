from hollarek.abstract.integer_inf import IntInf
from hollarek.devtools import Unittest

class TestIntInf(Unittest):

    def setUp(self):
        self.pos_inf = IntInf('+')
        self.neg_inf = IntInf('-')

    def test_sign_initialization(self):
        self.assertEqual(self.pos_inf.sign, '+')
        self.assertEqual(self.neg_inf.sign, '-')
        with self.assertRaises(ValueError):
            IntInf('invalid')

    def test_equality(self):
        self.assertTrue(self.pos_inf == IntInf('+'))
        self.assertFalse(self.pos_inf == self.neg_inf)

    def test_inequality(self):
        self.assertTrue(self.pos_inf != self.neg_inf)
        self.assertFalse(self.pos_inf != IntInf('+'))

    def test_less_than(self):
        self.assertTrue(self.neg_inf < self.pos_inf)
        self.assertFalse(self.pos_inf < self.neg_inf)
        self.assertTrue(self.neg_inf < 10)  # Negative infinity less than any real int
        self.assertFalse(self.pos_inf < 10)  # Positive infinity not less than any real int

    def test_less_than_or_equal(self):
        self.assertTrue(self.neg_inf <= self.pos_inf)
        self.assertTrue(self.neg_inf <= self.neg_inf)
        self.assertTrue(self.neg_inf <= 10)  # Negative infinity less than any real int
        self.assertFalse(self.pos_inf <= 10)  # Positive infinity not less than any real int

    def test_greater_than(self):
        self.assertTrue(self.pos_inf > self.neg_inf)
        self.assertFalse(self.neg_inf > self.pos_inf)
        self.assertTrue(self.pos_inf > 10)  # Positive infinity greater than any real int
        self.assertFalse(self.neg_inf > 10)  # Negative infinity not greater than any real int

    def test_greater_than_or_equal(self):
        self.assertTrue(self.pos_inf >= self.neg_inf)
        self.assertTrue(self.pos_inf >= self.pos_inf)
        self.assertTrue(self.pos_inf >= 10)  # Positive infinity greater than any real int
        self.assertFalse(self.neg_inf >= 10)  # Negative infinity not greater than any real int

    def test_addition(self):
        with self.assertRaises(ValueError):
            self.pos_inf + self.neg_inf

    def test_subtraction(self):
        with self.assertRaises(ValueError):
            self.pos_inf - self.neg_inf

    def test_not_implemented_operations(self):
        with self.assertRaises(NotImplementedError):
            self.pos_inf * 2
        with self.assertRaises(NotImplementedError):
            self.pos_inf / 2
        with self.assertRaises(NotImplementedError):
            self.pos_inf ** 2


if __name__ == "__main__":
    TestIntInf.execute_all()