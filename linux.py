import json
import os
import sys
import threading
import time
import requests

# pyinstaller need this imports here...
import netifaces
import psutil
import cpuinfo

from start import start


if __name__ == '__main__':
    start()