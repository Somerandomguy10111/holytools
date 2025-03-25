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
        a1 = MessageFormatter.get_boxed(text=msg)
        a2 = MessageFormatter.get_boxed(text=msg, headline='headline')

        i1 = ('+------+\n'
              '| msg1 |\n'
              '+------+\n')

        i2 = (f'+- headline -+\n'
              f'| msg1       |\n'
              f'+------------+\n')

        print(f'Expected box:\n{i1}')
        print(f'Actual box:\n{a1}')

        self.assertEqual(i1, a1)
        self.assertEqual(i2, a2)

    def test_multi_box_section(self):
        texts = ['msg2', 'msg2']
        headlines= ['h1', 'h2']

        actual_multi_box = MessageFormatter.multi_section_box(texts=texts, headlines=headlines)
        expected_multi_box=   ('+--- h1 ---+\n'
                               '| msg2     |\n'
                               '+--- h2 ---+\n'
                               '| msg2     |\n'
                               '+----------+\n')

        print(f'Expected multi box:\n{expected_multi_box}')
        print(f'Actual multi box:\n{actual_multi_box}')
        self.assertEqual(expected_multi_box, actual_multi_box)


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

