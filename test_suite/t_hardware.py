from hollarek.dev.hardware import PartitionInfo

if __name__ == '__main__':
    import psutil
    test_partitions = psutil.disk_partitions()
    print(test_partitions)

    test_part = PartitionInfo(device_name='/dev/nvme0n1p2')
    test_part.print_free_space_info()
    #
    # new_part = Partition.from_resource_path(resource_path='/media/daniel/STICKY1')
    # log(new_part.mount_point)
    # new_part.print_free_space_info()
    #
    # for p in partitions:
    #     print(p.mountpoint, psutil.disk