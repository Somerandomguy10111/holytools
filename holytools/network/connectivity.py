import subprocess  # For executing a shell command
import time

import tabulate


# ----------------------------

class ConnectivityTester:
    def __init__(self, remote_ip_addr : str = '172.217.12.131', remote_name : str = 'google.de'):
        self.remote_ip_addr : str = remote_ip_addr
        self.remote_name : str = remote_name

    def check_connectivity(self, duration : int = 30):
        start_time = time.time()
        ping_cycle_time = 1
        ping_results = {}
        latencies = {}
        hosts = [self.remote_ip_addr, self.remote_name]

        for h in hosts:
            ping_results[h] = []
            latencies[h] = []

        while time.time() - start_time < duration:
            for h in hosts:
                host_wait_time = ping_cycle_time*0.5
                is_reachable = self.is_ping_reachable(host_wait_time, host=h)
                remaining_time = host_wait_time - (time.time() - start_time) % host_wait_time

                ping_results[h].append(is_reachable)
                latencies[h].append(host_wait_time-remaining_time)
                if remaining_time > 0:
                    time.sleep(remaining_time)

            print(f'\nConnectivity results on {int(time.time() - start_time)}/{duration} seconds:')
            for h in hosts:
                ip_reachibility, latency = ping_results[h][-1], latencies[h][-1]
                msg = f'✓ (Latency: {latency*1000} ms)' if ip_reachibility else f'✗ (Timeout after {host_wait_time*1000}ms)'
                print(f'    - Connection to {h:<20}: {msg}')

        print(f'\nSummary of connectivity results:')
        table_data = []
        for h in hosts:
            uptime = sum(ping_results[h])*ping_cycle_time
            average_latency = sum(latencies[h])/len(latencies[h])
            row = [h, f'{uptime}/{duration}s', average_latency]
            table_data.append(row)
        col_headers = ['Host', 'Uptime', 'Average latency']
        print(tabulate.tabulate(tabular_data=table_data, headers=col_headers, tablefmt='psql'))

    @staticmethod
    def is_ping_reachable(timeout : float, host : str) -> bool:
        command = f'ping -w {timeout} -c 1 {host}'
        return subprocess.call(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True) == 0

if __name__ == "__main__":
    tester = ConnectivityTester(remote_name=f'music.youtube.com')
    tester.check_connectivity(duration=3)