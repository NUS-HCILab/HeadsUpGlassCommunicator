# coding=utf-8


import threading
import requests
import sys
import time
import os
import json

import glob
from pathlib import Path


def beep(times=1):
    for i in range(1, times):
        sys.stdout.write(f'\r\a{i}')
        sys.stdout.flush()
        time.sleep(0.4)
    sys.stdout.write('\n')
    time.sleep(0.1)


# return True if success else False
def send_request(url, data):
    print('sendRequest: {}, {}'.format(url, data))

    try:
        x = requests.post(url, data=str(data).encode('ascii', 'ignore'), timeout=3.5)
        print("{} \n".format(x.status_code))
        return True
    except Exception as e:
        print('Failed to send request', e.__class__)
        return False


def send_request_threaded(url, data):
    threading.Thread(target=send_request, args=(url, data)).start()


def sleep_seconds(seconds=0.2):
    count = 0
    delay_seconds = 0.05
    total_count = seconds * 20

    while count < total_count:
        count += 1
        time.sleep(delay_seconds)


def append_data(file_name, data):
    os.makedirs(os.path.dirname(file_name), exist_ok=True)

    try:
        file = open(file_name, "a")
        file.write(data)
        file.close()
    except Exception as e:
        print("Failed to write: ", e.__class__)


def is_file_exists(file_name):
    return os.path.exists(file_name)


# return lines
def read_file(file_name):
    with open(file_name) as f:
        lines = f.readlines()
    return lines


def write_data(file_name, lines):
    try:
        file = open(file_name, "w")
        file.writelines(lines)
        file.close()
    except Exception as e:
        print("Failed to write: ", e.__class__)


# extension: extension with . (e.g. .csv)
def read_file_names(directory, extension, prefix):
    all_files_with_extension = [file for file in glob.glob(f'{directory}/*{extension}')]
    all_files_with_extension.sort()
    # print(all_files_with_extension)
    return [file for file in all_files_with_extension if Path(file).stem.startswith(prefix)]


# save the json data {"key": "value", ...}
def save_json_data(file_name, json_data):
    try:
        with open(file_name, 'w') as outfile:
            json.dump(json_data, outfile)
    except Exception as e:
        print(f'Failed to save json data: {file_name}, {e.__class__}')


# return the saved json data {"key": "value", ...}
def read_json_data(file_name, maximum_age_in_minutes):
    if not os.path.exists(file_name):
        return {}

    # if data file is older than <maximum_age_in_minutes> ignore it
    if is_file_older_than(file_name, maximum_age_in_minutes * 60):
        return {}

    # read recent data file
    try:
        with open(file_name) as json_file:
            return json.load(json_file)
    except Exception as e:
        print(f'Failed to read order data: {file_name}, {e.__class__}')
        return {}


def is_file_older_than(file_name, seconds):
    file_time = os.path.getmtime(file_name)
    return (time.time() - file_time) > seconds
