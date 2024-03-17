from hollarek.logging import LogLevel
from hollarek.devtools import Unittest

class TestLoggin(Unittest):
    def test_info_error(self):
        self.log(f'Info text', level=LogLevel.INFO)
        self.log(f'Error text', level=LogLevel.ERROR)



if __name__ == '__main__':
    TestLoggin.execute_all()