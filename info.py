import netifaces
import platform
def collectInfos():
    # collect network interfaces

    # Get a list of all the network interfaces
    interfaces = netifaces.interfaces()

    # Create a dictionary to store the interface details
    interface_dict = {}

    # Loop through each interface and get its details
    for iface in interfaces:
        iface_details = netifaces.ifaddresses(iface)
        interface_dict[iface] = iface_details

    # Convert the dictionary to a JSON object
    networkInfos = (interface_dict)

    return {"network": networkInfos, "platform": {
        "machine": platform.machine(),
        "processor": platform.processor(),
        "uname": platform.uname(),
        "system": platform.system(),
        "release": platform.release(),
        "version": platform.version(),
        "system_alias": platform.system_alias(platform.system(), platform.release(), platform.version()),
    }}