import platform
import psutil


def calcMemOnLinux():
    memory = psutil.virtual_memory()

    # Get the total memory in bytes
    total_memory = memory.total

    # Get the used memory in bytes
    used_memory = memory.total - memory.available
    return used_memory
def calcMemOnMac():
    memory = psutil.virtual_memory()

    # Get the total memory in bytes
    total_memory = memory.total

    # Get the used memory in bytes
    used_memory = memory.total - memory.available

    return used_memory

def getUsedMemory():
    memory = psutil.virtual_memory()

    if platform.system() == 'Darwin':
        used= calcMemOnMac()
    else:
        used=calcMemOnLinux()

    return {'total': memory.total, 'used': used}