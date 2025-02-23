from __future__ import annotations
import time

from holytools.userIO import TrackedInt, MessageFormatter
from holytools.devtools import Unittest

class TestTrackedInt(Unittest):
    def test_incrementation(self):
        ti = TrackedInt(start_value=0, finish_value=10)
        for _ in range(20):
            ti += 1
            time.sleep(0.05)

    def test_incremenation_beyond_max_val(self):
        ti = TrackedInt(start_value=0, finish_value=10)
        for _ in range(20):
            ti += 1
            time.sleep(0.05)
        self.assertEqual(ti,20)

    def test_comparison(self):
        ti = TrackedInt(start_value=0, finish_value=10)
        is_smaller =  -1 < ti
        self.assertTrue(is_smaller)


class TestFormatter(Unittest):
    def test_get_boxed(self):
        msg = f'msg1'
        boxed = MessageFormatter.get_boxed(text=msg)
        headline_boxed = MessageFormatter.get_boxed(text=msg, headline='headline')

        intended_boxed = ('+------+\n'
                          '| msg1 |\n'
                          '+------+')

        intended_headline_boxed = (f'+- headline -+\n'
                                   f'| msg1       |\n'
                                   f'+------------+')

        self.assertTrue(intended_boxed == boxed)
        self.assertTrue(intended_headline_boxed == headline_boxed)

    def test_get_boxed_train(self):
        messages = ['msg1', 'msg2', 'msg3']
        boxed_train = MessageFormatter.get_boxed_train(messages=messages)

        intended_boxed_train = ('+------+     +------+     +------+\n'
                                '| msg1 |-----| msg2 |-----| msg3 |\n'
                                '+------+     +------+     +------+')
        print(f'Boxed train =\n{boxed_train}')
        print(f'Intended boxed train =\n{intended_boxed_train}')

        self.assertTrue(intended_boxed_train == boxed_train)

if __name__ == "__main__":
    TestFormatter.execute_all()
