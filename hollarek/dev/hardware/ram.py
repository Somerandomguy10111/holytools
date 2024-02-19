import psutil

def get_available_ram_in_GB(include_swap=False) -> float:
    available_memory = psutil.virtual_memory().available / (1024 ** 3)
    if include_swap:
        swap_memory = psutil.swap_memory().free / (1024 ** 3)
        available_memory += swap_memory
    return available_memory

def get_total_ram_in_GB(include_swap=False) -> float:
    total_memory = psutil.virtual_memory().total / (1024 ** 3)
    if include_swap:
        swap_memory = psutil.swap_memory().total / (1024 ** 3)
        total_memory += swap_memory

    return total_memory



if __name__ == '__main__':
    print(get_available_ram_in_GB(include_swap=True))
    print(get_total_ram_in_GB(include_swap=True))