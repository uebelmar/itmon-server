import netifaces
import platform

import psutil
import cpuinfo


def collectInfos():
    # Get a list of all the network interfaces
    interfaces = netifaces.interfaces()

    # Create a list to store the interface details
    interface_list = []

    # Loop through each interface and get its details
    for iface in interfaces:
        iface_details = netifaces.ifaddresses(iface)
        iface_info = {}

        iface_info['name'] = iface

        # Get the IPv4 address
        if netifaces.AF_INET in iface_details:
            ipv4_info = iface_details[netifaces.AF_INET][0]
            iface_info['ip_address'] = ipv4_info.get('addr')

        # Get the MAC address
        if netifaces.AF_LINK in iface_details:
            link_info = iface_details[netifaces.AF_LINK][0]
            iface_info['mac_address'] = link_info.get('addr')

        interface_list.append(iface_info)

    # Get the number of sockets and CPUs
    num_sockets = psutil.cpu_count(logical=False)
    cpu_info = psutil.cpu_freq(percpu=True)

    # Create a list to store the details of each CPU
    cpu_list = []

    # Loop through each CPU and get its details
    info = cpuinfo.get_cpu_info()
    for cpu in cpu_info:
        cpu_dict = {}
        cpu_dict["clock_speed"] = cpu.current
        cpu_dict["name"] = info["brand_raw"]
        cpu_dict["model"] = info["model"]

        cpu_list.append(cpu_dict)

    return {"network": interface_list,
            "platform": {
                "machine": platform.machine(),
                "processor": platform.processor(),
                "uname": platform.uname(),
                "system": platform.system(),
                "release": platform.release(),
                "version": platform.version(),
                "system_alias": platform.system_alias(platform.system(), platform.release(), platform.version()),
                "num_sockets": num_sockets,
                "cpus": cpu_list
            }}
