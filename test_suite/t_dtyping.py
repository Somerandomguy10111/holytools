from types import NoneType
from typing import Optional, Union

from hollarek.dev import Unittest
from hollarek.dev.dtyping.get_core import is_optional_type


class TestIsOptionalType(Unittest):
    def test_optional_type(self):
        self.assertTrue(is_optional_type(Optional[int]))
        self.assertTrue(is_optional_type(Union[None, int]))
        self.assertTrue(is_optional_type(Union[int, None]))

    def test_non_optional_type(self):
        self.assertFalse(is_optional_type(int))
        self.assertFalse(is_optional_type(Union[int, str]))
        self.assertFalse(is_optional_type(float))

    def test_complex_optional_type(self):
        self.assertTrue(is_optional_type(Optional[Union[int, str]]))
        self.assertTrue(is_optional_type(Union[None, int, str]))

    def test_none_type(self):
        self.assertFalse(is_optional_type(None))
        self.assertFalse(is_optional_type(NoneType))

    def setUp(self):
        pass
