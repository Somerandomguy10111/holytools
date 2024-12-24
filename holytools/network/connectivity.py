import subprocess  # For executing a shell command
import time

import tabulate


# ----------------------------

class ConnectivityTester:
    def __init__(self, remote_ip_addr : str = '172.217.12.131', remote_name : str = 'google.de'):
        self.remote_ip_addr : str = remote_ip_addr
        self.remote_name : str = remote_name

    def check_connectivity(self, max_duration : int = 30):
        hosts = [self.remote_ip_addr, self.remote_name]
        ping_timeout = 1
        poll_duration = ping_timeout*len(hosts)

        ping_results = {}
        latencies = {}
        for h in hosts:
            ping_results[h] = []
            latencies[h] = []

        start_time = time.time()
        while time.time() - start_time < max_duration:
            for h in hosts:
                is_reachable = self.is_ping_reachable(ping_timeout, host=h)
                remaining_time = ping_timeout - (time.time() - start_time) % ping_timeout

                ping_results[h].append(is_reachable)
                latencies[h].append(ping_timeout-remaining_time)
                if remaining_time > 0:
                    time.sleep(remaining_time)

            print(f'\nConnectivity results on {int(time.time() - start_time)}/{max_duration} seconds:')
            for h in hosts:
                ip_reachibility, latency = ping_results[h][-1], latencies[h][-1]
                msg = f'✓ (Latency: {latency*1000} ms)' if ip_reachibility else f'✗ (Timeout after {ping_timeout*1000}ms)'
                print(f'    - Connection to {h:<20} {msg}')

        print(f'\nSummary of connectivity results:')
        table_data = []
        for h in hosts:
            polled_duration = poll_duration*len(ping_results[h])

            uptime = sum(ping_results[h])*poll_duration
            average_latency = f'{sum(latencies[h])/len(latencies[h])*1000:.2f}ms'
            row = [h, f'{uptime}/{polled_duration}s', average_latency]
            table_data.append(row)
        col_headers = ['Host', 'Uptime', 'Average latency']
        print(tabulate.tabulate(tabular_data=table_data, headers=col_headers, tablefmt='psql'))

    @staticmethod
    def is_ping_reachable(timeout : int, host : str) -> bool:
        if timeout < 1:
            raise ValueError('Timeout must be at least 1 second')

        command = f'ping -w {timeout} -c 1 {host}'
        return subprocess.call(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True) == 0

if __name__ == "__main__":
    tester = ConnectivityTester(remote_name=f'music.youtube.com')
    tester.check_connectivity(max_duration=3600)