import psutil

from memory import getUsedMemory


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
            "available": usage.free
        })

    # convert the list of JSON objects to a JSON array
    harddiskInfo = (partition_data)

    # memory

    data = {
        "cpu": {
            "cores": (cpu_loads),
            "total": cpu_load_percent
        },
        "harddisks": harddiskInfo,
        "memory": getUsedMemory()
    }
    return data