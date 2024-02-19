from typing import Optional
from hollarek.dev.log import get_logger, LogSettings
import logging
import os
import psutil
# -------------------------------------------


drive_logger = get_logger(settings=LogSettings(include_call_location=False))
def log(msg : str, level : int = logging.INFO):
    drive_logger.log(msg=msg, level=level)
    print(drive_logger.name)


class PartitionInfo:
    @classmethod
    def from_resource_path(cls, resource_path : str):
        device_name = find_device_of_path(resource_path=resource_path)
        return cls(device_name=device_name)

    def __init__(self, device_name: str):
        self.mount_point : str = get_device_mount_point(device_name=device_name)
        if not self.mount_point:
            raise ResourceWarning(f'Could not find mount point for device {device_name}')

        self.device_name : str = device_name


    def print_free_space_info(self):
        warning_free_space = 250
        critical_free_space_in_GB = 100

        free_space_GB = int(round(self.get_free_space_in_GB(), 0))
        total_space_GB = int(round(self.get_total_space_in_GB(), 0))
        log(f'Free space on partition {self.device_name}: {free_space_GB}/{total_space_GB} GB')

        if free_space_GB < critical_free_space_in_GB:
            log(f'Warning: Almost no disk space remaining on {self.device_name}. Only {free_space_GB} GB left!', level=logging.CRITICAL)
        elif free_space_GB < warning_free_space:
            log(f'Warning: Disk space is running low on "{self.device_name}". Only {free_space_GB} GB left!', level=logging.WARNING)


    def get_free_space_in_GB(self) -> float:
        stats = psutil.disk_usage(self.mount_point)
        return stats.free / (1024 ** 3)

    def get_total_space_in_GB(self) -> float:
        stats = psutil.disk_usage(self.mount_point)
        return stats.total / (1024 ** 3)

def find_device_of_path(resource_path: str) -> Optional[str]:
    absolute_path = os.path.abspath(resource_path)

    partitions = psutil.disk_partitions(all=True)
    partitions.sort(key=lambda x: len(x.mountpoint), reverse=True)

    for partition in partitions:
        if absolute_path.startswith(partition.mountpoint):
            return partition.device

    return None


def get_device_mount_point(device_name : str) -> Optional[str]:
    partitions = psutil.disk_partitions()
    for part in partitions:
        if part.device == device_name:
            return part.mountpoint
    return None


if __name__ == '__main__':
    test_partitions = psutil.disk_partitions()
    print(test_partitions)

    test_part = PartitionInfo(device_name='/dev/nvme0n1p2')
    log(test_part.mount_point)
    test_part.print_free_space_info()

    # new_part = Partition.from_resource_path(resource_path='/media/daniel/STICKY1')
    # log(new_part.mount_point)
    # new_part.print_free_space_info()
    #
    # for p in partitions:
    #     print(p.mountpoint, psutil.disk_usage(p.mountpoint).percent)