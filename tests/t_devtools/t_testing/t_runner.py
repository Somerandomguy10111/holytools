import requests
from flask import Flask, jsonify

from holytools.devtools import Unittest
from holytools.devtools.testing.unit import BlockedTester

# ------------------------------------------------------------------

# Flask App
app = Flask(__name__)
the_bool = False

host = 'localhost'
port = 8000

@app.route('/toggle', methods=['GET'])
def toggle():
    global the_bool
    the_bool = True
    return jsonify({'status': 'success'})

class ServerTester(BlockedTester):
    def blocked(self):
        app.run(host=host, port=port)

    @staticmethod
    def perform_check() -> bool:
        requests.get(url=f'http://{host}:{port}/toggle')
        return the_bool == True


class TestBlockedTester(Unittest):
    def test_run(self):
        tester = ServerTester()
        self.assertTrue(tester.check_ok(check_func=tester.perform_check, delay=1))


if __name__ == "__main__":
    TestBlockedTester.execute_all()