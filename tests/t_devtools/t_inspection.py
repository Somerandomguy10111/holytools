from typing import Optional, Union

from holytools.devtools import ModuleInspector, Unittest, Argument, TypeInspector


class SampleClass:
    def method_with_args(self, arg1 : int, arg2 : str='default'):
        pass

    def _private_method(self):
        pass

    def __magic_method__(self):
        pass

    @staticmethod
    def static():
        pass

    @classmethod
    def classmthd(cls):
        pass

def valid(arg1: int, arg2: int = 42):
    _, __ = arg1, arg2

def invalid(arg1, arg2=42):
    _, __ = arg1, arg2


class InheritedClass(SampleClass):
    pass

    def new(self):
        pass


class TestArgument(Unittest):
    def test_set_default(self):
        arg = Argument(name='arg1', dtype=int)
        arg.set_default_val(99)
        self.assertEqual(arg.get_default_val(), 99)

    def test_has_default(self):
        arg = Argument(name='arg1', dtype=int)
        self.assertFalse(arg.has_default_val())
        arg.set_default_val(99)
        self.assertTrue(arg.has_default_val())

    def test_get_default_val(self):
        arg = Argument(name='arg1', dtype=int)
        arg.set_default_val(99)
        self.assertEqual(arg.get_default_val(), 99)
        arg2 = Argument(name='arg2', dtype=int)
        with self.assertRaises(AttributeError):
            arg2.get_default_val()


class TestGetArgs(Unittest):
    def test_with_hints(self):
        args = ModuleInspector.get_args(valid)
        self.assertEqual(len(args), 2)
        self.assertIsInstance(args[0], Argument)
        self.assertEqual(args[0].name, 'arg1')
        self.assertEqual(args[0].dtype, int)
        self.assertTrue(not args[0].has_default_val())
        self.assertEqual(args[1].name, 'arg2')
        self.assertEqual(args[1].dtype, int)
        self.assertEqual(args[1].get_default_val(), 42)

    def test_no_hints(self):
        with self.assertRaises(ValueError):
            ModuleInspector.get_args(invalid)

    def test_unbound_include_self(self):
        with self.assertRaises(ValueError):
            ModuleInspector.get_args(SampleClass.method_with_args, exclude_self=False)

    def test_bound_include_self(self):
        sc = SampleClass()
        args = ModuleInspector.get_args(sc.method_with_args, exclude_self=False)
        self.assertEqual(args[0].name, 'self')

    def test_with_inheritance(self):
        methods = ModuleInspector.get_methods(InheritedClass)
        self.assertIn(InheritedClass.method_with_args, methods)
        self.assertIn(InheritedClass._private_method, methods)
        self.assertNotIn(InheritedClass.__magic_method__, methods, "Magic methods should not be included by default")

    def test_without_inhertiance(self):
        methods = ModuleInspector.get_methods(InheritedClass, include_inherited=False)
        self.assertNotIn(InheritedClass.method_with_args, methods)
        self.assertNotIn(InheritedClass._private_method, methods)
        self.assertNotIn(InheritedClass.__magic_method__, methods)
        self.assertIn(InheritedClass.new, methods)


class TestGetMethods(Unittest):
    def test_default(self):
        methods = ModuleInspector.get_methods(SampleClass)
        self.assertIn(SampleClass.method_with_args, methods)
        self.assertIn(SampleClass._private_method, methods)
        self.assertNotIn(SampleClass.__magic_method__, methods)

    def test_exclude_private(self):
        methods = ModuleInspector.get_methods(SampleClass, public_only=True)
        self.assertIn(SampleClass.method_with_args, methods)
        self.assertNotIn(SampleClass._private_method, methods)

    def test_include_operators(self):
        methods = ModuleInspector.get_methods(SampleClass, include_operators=True)
        self.assertIn(SampleClass.__magic_method__, methods)



if __name__ == '__main__':
    # TestGetMethods.execute_all()
    TestGetArgs.execute_all()
    # TestArgument.execute_all()


class TestOptionalTyping(Unittest):
    @classmethod
    def setUpClass(cls):
        cls.optional_int= Optional[int]
        cls.union_none_int= Union[None, int]
        cls.nested_optional = Optional[Union[int,str]]
        cls.triple_union = Union[None, int, str]


    def test_optional_type(self):
        optional_types = [self.optional_int, self.union_none_int]
        for dtype in optional_types:
            self.assertTrue(TypeInspector.is_optional_type(dtype), msg=f'\"{dtype}\" should be recognized as Optional')

    def test_complex_optional_type(self):
        for dtype in [self.nested_optional, self.triple_union]:
            self.assertTrue(TypeInspector.is_optional_type(dtype), msg=f'\"{dtype}\" should be recognized as Optional')


    def test_non_optional_type(self):
        for dtype in [int, Union[int, str], float]:
            self.assertFalse(TypeInspector.is_optional_type(dtype), msg=f'\"{dtype}\" should not be recognized as Optional')
