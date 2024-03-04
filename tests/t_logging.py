# from hollarek.logging import add_color, Color
# 
# abc = add_color(msg='hi', color=Color.RED)
# d = ' there'
# e =  add_color(msg=' my dude', color=Color.GREEN)
# print(abc+d+e)
from hollarek.logging import Loggable, LogSettings, get_logger

class NewClass(Loggable):
    def __init__(self):
        super().__init__(settings=LogSettings(call_location=True))

    def say_hi(self):
        self.log(msg='hi there')

a = NewClass()
a.say_hi()


new_logger = get_logger(LogSettings(call_location=True))
new_logger.log(f'new')