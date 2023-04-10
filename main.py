# This is a sample Python script.
import json
import os

import threading
import time


import requests

from info import collectInfos
from metrics import collectMetrics


# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

def iterateInfos():
    while True:
        data = collectInfos()
        # Get the current time in seconds since the Epoch
        current_utc_time = time.time()

        # Convert the current time to a MySQL datetime format
        postData = ({
            "datetime": time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(current_utc_time)),
            "token": config['token'],
            "data": data
        })
        print(postData)

        # send to server
        url = config['apiUrl'] + '/servers/info'
        headers = {'Content-Type': 'application/json'}

        response = requests.post(url, headers=headers, data=json.dumps(postData))
        responseContent = response.content.decode('utf-8')  # Decode the content from bytes to a string if necessary
        print(responseContent)
        time.sleep(60 * 24)  # 60min * 24std = 1x/tag





def iterateMetrics():
    while True:
        data = collectMetrics()
        # Get the current time in seconds since the Epoch
        current_utc_time = time.time()

        # Convert the current time to a MySQL datetime format
        postData = ({
            "datetime": time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(current_utc_time)),
            "token": config['token'],
            "data": data
        })
        print(postData)

        # send to server
        url = config['apiUrl'] + '/servers/metrics'
        headers = {'Content-Type': 'application/json'}

        start_time = time.time()

        response = requests.post(url, headers=headers, data=json.dumps(postData))
        end_time = time.time()
        print("Response time for metrics:", end_time - start_time)

        responseContent = response.content.decode('utf-8')  # Decode the content from bytes to a string if necessary
        print(responseContent)
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
