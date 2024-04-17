import logging
from hollarek.core.logging import LogLevel, get_logger
from hollarek.devtools import Unittest
# from PIL import Image




class TestLoggin(Unittest):
    def test_info_error(self):
        self.log(f'Info text', level=LogLevel.INFO)
        self.log(f'Error text', level=LogLevel.ERROR)

    def test_get_logger(self):
        logger_name = "basic_xyz_logger"
        _ = get_logger(name=logger_name)

        logger_is_registered = logger_name in logging.root.manager.loggerDict
        self.assertTrue(logger_is_registered)


if __name__ == '__main__':
    TestLoggin.execute_all()