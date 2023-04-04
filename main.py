# This is a sample Python script.
import time
import psutil
import json
import os


# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


def do():
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
    harddiskInfo = json.dumps(partition_data)

    # memory
    memory = psutil.virtual_memory()

    # Get the total memory in bytes
    total_memory = memory.total

    # Get the used memory in bytes
    used_memory = memory.used

    data = {
        "cpu": {
            "cores": (cpu_loads),
            "total": cpu_load_percent
        },
        "harddisks": harddiskInfo,
        "memory": {
            "total": total_memory,
            "used_memory": used_memory

        }
    }
    print(data)


if __name__ == '__main__':
    __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))
    filename = os.path.join(__location__, 'itmon.config.json')
    if os.path.exists(filename):
        with open('config.json', 'r') as f:
            config = json.load(f)
    else:
        print("Config-File does not exist.")
        exit()
    while True:
        do()
        time.sleep(config['interval'])
