from typing import Callable

from holytools.devtools import ModuleInspector, Unittest
from tests.t_devtools.t_module.modules import SampleClass, InheritedClass


# ----------------------------------------------------------------------------------------

class TestGetMethods(Unittest):
    def test_get_bound(self):
        for obj in [SampleClass, SampleClass()]:
            m = [m for m in ModuleInspector.get_methods(obj) if m.__name__ == SampleClass.method_with_args.__name__][0]
            is_bound = hasattr(m, '__self__')
            is_obj = not isinstance(obj, type)
            self.assertEqual(is_bound, is_obj)

    def test_default_behaviour(self):
        for obj in [SampleClass, SampleClass()]:
            methods = ModuleInspector.get_methods(obj)
            method_names = self.get_mthd_names(methods)
            self.assertIn(SampleClass.method_with_args.__name__, method_names)
            self.assertNotIn(SampleClass._private_method.__name__, method_names)
            self.assertNotIn(SampleClass.__magic_method__.__name__, method_names)

    def test_exclude_private(self):
        for obj in [SampleClass, SampleClass()]:
            methods = ModuleInspector.get_methods(obj, include_private=False)
            method_names = self.get_mthd_names(methods)
            self.assertIn(SampleClass.method_with_args.__name__, method_names)
            self.assertNotIn(SampleClass._private_method.__name__, method_names)

    def test_include_magic(self):
        for obj in [SampleClass, SampleClass()]:
            methods = ModuleInspector.get_methods(obj, include_magic_methods=True)
            method_names = self.get_mthd_names(methods)
            self.assertIn(SampleClass.__magic_method__.__name__, method_names)

    def test_inheritance_flag(self):
        for obj in [InheritedClass(), InheritedClass]:
            methods = ModuleInspector.get_methods(obj, include_inherited=True)
            method_names = self.get_mthd_names(methods)
            self.assertIn(InheritedClass.method_with_args.__name__, method_names)
            self.assertIn(InheritedClass.new.__name__, method_names)

        for obj in [InheritedClass(), InheritedClass]:
            methods = ModuleInspector.get_methods(obj, include_inherited=False)
            method_names = self.get_mthd_names(methods)
            self.assertNotIn(InheritedClass.method_with_args.__name__, method_names)
            self.assertIn(InheritedClass.new.__name__, method_names)

    @staticmethod
    def get_mthd_names(methods : list[Callable]) -> list[str]:
        return [m.__name__ for m in methods]

if __name__ == '__main__':
    TestGetMethods.execute_all()
