# This is a sample Python script.
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

from info import collectInfos
from metrics import collectMetrics

from multiprocessing import freeze_support

freeze_support()


def check_response(response):
    if response.status_code != 200 or ("debug" in config and config['debug'] is True):
        print(f"Server response code: {response.status_code}")
        print(f"Server response text: {response.text}")


def iterateInfos():
    while True:
        data = collectInfos()
        # Get the current time in seconds since the Epoch
        current_utc_time = time.time()

        # Convert the current time to a MySQL datetime format
        postData = ({
            "agent_version": 1.0,
            "datetime": time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(current_utc_time)),
            "token": config['token'],
            "data": data
        })

        # send to server
        url = config['apiUrl'] + '/servers/info'
        headers = {'Content-Type': 'application/json', 'Accept-Encoding': 'gzip'}

        response = requests.post(url, headers=headers, data=json.dumps(postData))
        check_response(response)
        time.sleep(60 * 24)  # 60min * 24std = 1x/tag


def iterateMetrics():
    while True:
        data = collectMetrics()
        # Get the current time in seconds since the Epoch
        current_utc_time = time.time()

        # Convert the current time to a MySQL datetime format
        postData = ({
            "agent_version": 1.0,
            "datetime": time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(current_utc_time)),
            "token": config['token'],
            "data": data
        })
        if "debug" in config and config['debug'] is True:
            print(postData)

        # send to server
        url = config['apiUrl'] + '/servers/metrics'
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, headers=headers, data=json.dumps(postData))
        check_response(response)
        del data
        del postData
        time.sleep(20)


if __name__ == '__main__':
    if getattr(sys, 'frozen', False):
        # If the application is run as a bundle, the PyInstaller bootloader
        # extends the sys module by a flag frozen=True and sets the app
        # path into variable _MEIPASS'.
        application_path = os.path.dirname(sys.executable)
    else:
        application_path = os.path.dirname(os.path.abspath(__file__))

    # check if there is a config for local environment
    filename = os.path.join(application_path, 'itmon.config.localhost.json')
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            config = json.load(f)

    else:
        filename = os.path.join(application_path, 'itmon.config.json')
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                config = json.load(f)
        else:
            print("Config-File does not exist in " + application_path)
            exit()

    # check if token is in config
    if 'apiUrl' not in config:
        print("apiUrl not supplied in config.")
        exit()
    if 'token' not in config:
        print("token not supplied in config.")
        exit()

    threadIterateMetrics = threading.Thread(target=iterateMetrics)
    threadIterateMetrics.start()

    threadIterateInfos = threading.Thread(target=iterateInfos)
    threadIterateInfos.start()
