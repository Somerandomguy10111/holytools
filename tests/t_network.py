from holytools.devtools import Unittest
from holytools.network import IpProvider, NetworkArea

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

if __name__ == '__main__':
    TestIpProvider.execute_all()
