# from api.network import Socket
# from api import NetworkArea
# from hollarek.devtools import Unittest
#
# class TestNetwork(Unittest):
#
#     def test_init_default_sockets(self):
#         network = Network()
#         self.assertEqual(network.webapp_socket.ip, network._get_host(area=NetworkArea.LOCALHOST))
#         self.assertEqual(network.webapp_socket.port, 5000)
#         self.assertEqual(network.engine_socket.ip, network._get_host(area=NetworkArea.LOCALHOST))
#         self.assertEqual(network.engine_socket.port, 5001)
#
#     def test_init_custom_sockets(self):
#         custom_webapp_socket = Socket(ip="192.168.1.10", port=6000)
#         custom_engine_socket = Socket(ip="192.168.1.11", port=6001)
#         network = Network(webapp_socket=custom_webapp_socket, engine_socket=custom_engine_socket)
#         self.assertEqual(network.webapp_socket, custom_webapp_socket)
#         self.assertEqual(network.engine_socket, custom_engine_socket)
#
#
#     def test_host(self):
#         self.assertEqual(Network._get_host(NetworkArea.LOCALHOST), '127.0.0.1')
#         self.assertIsInstance(Network._get_private_ip(), str)
#         with self.assertRaises(PermissionError):
#             Network._get_host(NetworkArea.GLOBAL)
#
#     def test_get_public_ip_addr(self):
#         ip_addr = IP._get_public_ip()
#         self.assertIsInstance(ip_addr, str)
#         self.log(f'Public ip addr is {ip_addr}')
#
#     def test_get_private_ip_addr(self):
#         ip_addr = Network._get_private_ip()
#         self.assertIsInstance(ip_addr, str)
#         self.log(f'Private ip addr is {ip_addr}')
#
# if __name__ == '__main__':
#     TestNetwork.execute_all()
