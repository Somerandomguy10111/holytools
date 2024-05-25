import logging
from holytools.logging import LogLevel, LoggerFactory
from holytools.devtools import Unittest

class TestLoggin(Unittest):
    def test_info_error(self):
        self.log(f'Info text', level=LogLevel.INFO)
        self.log(f'Error text', level=LogLevel.ERROR)

    def test_make_logger(self):
        logger_name = "basic_xyz_logger"
        _ = LoggerFactory.make_logger(name=logger_name)

    def test_retrieve_logger(self):
        logger_name = 'this_unique_logger'

        expected_logger = LoggerFactory.make_logger(name=logger_name)
        actual_logger = logging.getLogger(name=logger_name)
        self.assertEqual(expected_logger, actual_logger)
        logger_is_registered = logger_name in logging.root.manager.loggerDict
        self.assertTrue(logger_is_registered)

if __name__ == '__main__':
    TestLoggin.execute_all()