import psutil
from memory import getUsedMemory


import psutil

def get_process_info():
    process_list = []

    for process in psutil.process_iter(['pid', 'name', 'memory_info', 'cpu_percent']):
        try:
            pid = process.info.get('pid', None)
            name = process.info.get('name', None)
            mem_info = process.info.get('memory_info', None)
            cpu_percent = process.info.get('cpu_percent', None)

            if mem_info is not None:
                mem_usage_mib = mem_info.rss / (1024 * 1024)
            else:
                mem_usage_mib = None

            process_info = {
                "PID": pid,
                "Name": name,
                "Memory Usage (MiB)": f"{mem_usage_mib:.2f}" if mem_usage_mib is not None else None,
                "CPU Usage (%)": cpu_percent
            }
            process_list.append(process_info)

        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    return process_list



def collectMetrics():
    # Get CPU load as a percentage over the last 5 seconds
    cpu_loads = psutil.cpu_percent(percpu=True)
    cpu_load_percent = psutil.cpu_percent()

    # harddisk

    partitions = psutil.disk_partitions()

    # create a list to hold the JSON objects for each partition
    partition_data = []

    # iterate over each partition and add its data to the list
    for partition in partitions:
        usage = psutil.disk_usage(partition.mountpoint)
        partition_data.append({
            "mountpoint": partition.mountpoint,
            "total": usage.total,
            "available": usage.free,
            "used": usage.used
        })

    # convert the list of JSON objects to a JSON array
    harddiskInfo = (partition_data)

    # memory

    data = {
      #  "processes": get_process_info(),
        "cpu": {
            "cores": (cpu_loads),
            "total": cpu_load_percent
        },
        "harddisks": harddiskInfo,
        "memory": getUsedMemory()
    }
    del cpu_loads
    del cpu_load_percent
    del partitions
    del partition_data
    del harddiskInfo

    return data