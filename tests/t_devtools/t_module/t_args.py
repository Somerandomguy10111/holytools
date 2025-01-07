from holytools.devtools import Unittest, ModuleInspector, Argument
from tests.t_devtools.t_module.modules import valid_function, invalid_function, SampleClass


class TestGetArgs(Unittest):
    def test_get_args(self):
        args = ModuleInspector.get_args(valid_function)
        self.assertEqual(len(args), 2)
        self.assertIsInstance(args[0], Argument)
        self.assertEqual(args[0].name, 'arg1')
        self.assertEqual(args[0].dtype, int)
        self.assertTrue(not args[0].has_default_val())

        self.assertEqual(args[1].name, 'arg2')
        self.assertEqual(args[1].dtype, int)
        self.assertEqual(args[1].get_default_val(), 42)

        with self.assertRaises(ValueError):
            ModuleInspector.get_args(invalid_function)

    def test_exclude_self(self):
        a1 = ModuleInspector.get_args(valid_function, exclude_self=True)
        a2 = ModuleInspector.get_args(valid_function, exclude_self=False)
        self.assertEqual(a1, a2)

        sc = SampleClass()
        args = ModuleInspector.get_args(sc.method_with_args, exclude_self=False)
        self.assertEqual(args[0].name, 'self')

        args = ModuleInspector.get_args(sc.method_with_args, exclude_self=True)
        self.assertNotEqual(args[0].name, 'self')


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

if __name__ == "__main__":
    TestArgument.execute_all()
    TestGetArgs.execute_all()