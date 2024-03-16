from hollarek.logging import Loggable, LogSettings, get_logger, LogLevel
from hollarek.devtools import Unittest

class TestLoggin(Unittest):
    def test_info_error(self):
        self.log(f'Info text', level=LogLevel.INFO)
        self.log(f'Error text', level=LogLevel.ERROR)



if __name__ == '__main__':
    TestLoggin.execute_all()