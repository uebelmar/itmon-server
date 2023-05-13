# This is a sample Python script.
import json
import os
import threading
import time
import requests

from info import collectInfos
from metrics import collectMetrics


def check_response(response):
    if response.status_code != 200:
        print(f"Error: Received status code {response.status_code} instead of 200.")
        print(f"Server response: {response.text}")

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
        if "localhost" in config and config['localhost'] == True:
            print(postData)

        # send to server
        url = config['apiUrl'] + '/servers/metrics'
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, headers=headers, data=json.dumps(postData))
        check_response(response)
        del data
        del postData
        time.sleep(config['interval'])


if __name__ == '__main__':
    __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))

    # check if there is a config for local environment
    filename = os.path.join(__location__, 'itmon.config.localhost.json')
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            config = json.load(f)

    else:
        filename = os.path.join(__location__, 'itmon.config.json')
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                config = json.load(f)
        else:
            print("Config-File does not exist.")
            exit()
    threadIterateMetrics = threading.Thread(target=iterateMetrics)
    threadIterateMetrics.start()

    threadIterateInfos = threading.Thread(target=iterateInfos)
    threadIterateInfos.start()
