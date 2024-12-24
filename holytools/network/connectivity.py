import subprocess  # For executing a shell command
import time
import tabulate


# ----------------------------

class ConnectivityTester:
    def __init__(self, remote_ip_addr : str = '172.217.12.131', remote_name : str = 'google.de'):
        self.remote_ip_addr : str = remote_ip_addr
        self.remote_name : str = remote_name

    def check_connectivity(self, max_duration : int = 30, verbose : bool = False):
        hosts = [self.remote_ip_addr, self.remote_name]
        ping_timeout = 1
        poll_duration = ping_timeout*len(hosts)

        ping_results = {}
        latencies = {}
        for h in hosts:
            ping_results[h] = []
            latencies[h] = []

        print(f'Launching connectivity tests for {self.remote_name} = {self.remote_ip_addr}...')
        start_time = time.time()
        while time.time() - start_time < max_duration:
            for h in hosts:
                is_reachable = self.is_ping_reachable(ping_timeout, host=h)
                remaining_time = ping_timeout - (time.time() - start_time) % ping_timeout

                ping_results[h].append(is_reachable)
                latencies[h].append(ping_timeout-remaining_time)
                if remaining_time > 0:
                    time.sleep(remaining_time)

            if not verbose:
                continue

            print(f'\nConnectivity results on {int(time.time() - start_time)}/{max_duration} seconds:')
            for h in hosts:
                ip_reachibility, latency = ping_results[h][-1], latencies[h][-1]
                msg = f'✓ (Latency: {latency*1000} ms)' if ip_reachibility else f'✗ (Timeout after {ping_timeout*1000}ms)'
                print(f'    - Connection to {h:<20} {msg}')

        print(f'Summary of connectivity results:')
        table_data = []
        for h in hosts:
            polled_duration = poll_duration*len(ping_results[h])

            uptime = sum(ping_results[h])*poll_duration
            average_latency = f'{sum(latencies[h])/len(latencies[h])*1000:.2f}ms'
            row = [h, f'{uptime}/{polled_duration}s', average_latency]
            table_data.append(row)
        col_headers = ['Host', 'Uptime', 'Average latency']
        print(tabulate.tabulate(tabular_data=table_data, headers=col_headers, tablefmt='psql'))
        print()

    @staticmethod
    def is_ping_reachable(timeout : int, host : str) -> bool:
        if timeout < 1:
            raise ValueError('Timeout must be at least 1 second')

        command = f'ping -w {timeout} -c 1 {host}'
        return subprocess.call(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True) == 0

if __name__ == "__main__":
    duration = 10
    tester = ConnectivityTester(remote_name=f'music.youtube.com', remote_ip_addr='142.250.184.238')
    tester.check_connectivity(max_duration=duration)

    geeksforgeeks = ('www.geeksforgeeks.com', '199.59.243.227')
    tester2 = ConnectivityTester(remote_name=geeksforgeeks[0], remote_ip_addr=geeksforgeeks[1])
    tester2.check_connectivity(max_duration=duration)

    ibm = ('www.ibm.com', '23.37.59.85')
    tester3 = ConnectivityTester(remote_name=ibm[0], remote_ip_addr=ibm[1])
    tester3.check_connectivity(max_duration=duration)