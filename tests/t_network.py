import time

from holytools.devtools import Unittest
from holytools.network import IpProvider, NetworkArea, Endpoint
from flask import Flask, request
from multiprocessing import Process


class TestIpProvider(Unittest):
    def get_ip(self):
        self.assertEqual(IpProvider.get_localhost(), '127.0.0.1')
        self.assertIsInstance(IpProvider.get_private_ip(), str)
        with self.assertRaises(PermissionError):
            IpProvider.get_ip(NetworkArea.GLOBAL)

    def test_get_public_ip_addr(self):
        ip_addr = IpProvider.get_public_ip()
        self.assertIsInstance(ip_addr, str)
        self.log(f'Public ip addr is {ip_addr}')

    def test_get_private_ip_addr(self):
        ip_addr = IpProvider.get_private_ip()
        self.assertIsInstance(ip_addr, str)
        self.log(f'Private ip addr is {ip_addr}')


class TestEndpoint(Unittest):
    @classmethod
    def setUpClass(cls):
        def run_app():
            app = Flask(__name__)

            @app.route('/test', methods=['GET', 'POST'])
            def test():
                if request.method == 'GET':
                    return 'GET request received', 200
                elif request.method == 'POST':
                    data = request.data.decode('utf-8')
                    return f'POST request received with data: {data}', 200

            app.run(host='127.0.0.1', port=8080)

        process = Process(target=run_app)
        process.start()

        endpoint = Endpoint.make_localhost(port=8080, path='/test')
        cls.endpoint = endpoint
        time.sleep(1)

    def test_get_url(self):
        url = self.endpoint.get_url(protocol=f'http')
        self.assertIsInstance(url, str)

    def test_post(self):
        response = self.endpoint.post('Hello World', secure=False)
        self.assertEqual(response.status_code, 200)

    def test_get(self):
        response = self.endpoint.get(secure=False)
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    TestEndpoint.execute_all()
