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
    if response.status_code != 200 or ("debug" in jsonConfig and jsonConfig['debug'] is True):
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
            "token": jsonConfig['token'],
            "data": data
        })

        if "debug" in jsonConfig and jsonConfig['debug'] is True:
            print(postData)

        # send to server
        url = jsonConfig['apiUrl'] + '/servers/info'
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
            "token": jsonConfig['token'],
            "data": data
        })
        if "debug" in jsonConfig and jsonConfig['debug'] is True:
            print(postData)

        # send to server
        url = jsonConfig['apiUrl'] + '/servers/metrics'
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, headers=headers, data=json.dumps(postData))
        check_response(response)

        del data
        del postData
        time.sleep(20)


def start():
    global jsonConfig
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
            jsonConfig = json.load(f)

    else:
        filename = os.path.join(application_path, 'itmon.config.json')
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                jsonConfig = json.load(f)
        else:
            print("Config-File does not exist in " + application_path)
            sys.exit(123)

    # check if token is in jsonConfig
    if 'apiUrl' not in jsonConfig:
        print("apiUrl not supplied in config.")
        sys.exit(4566)
    if 'token' not in jsonConfig:
        print("token not supplied in config.")
        sys.exit(789)

    threadIterateMetrics = threading.Thread(target=iterateMetrics)
    threadIterateMetrics.start()

    threadIterateInfos = threading.Thread(target=iterateInfos)
    threadIterateInfos.start()

    while True:
        time.sleep(10)
