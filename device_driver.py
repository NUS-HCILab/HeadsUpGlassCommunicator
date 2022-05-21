# coding=utf-8

import display_formatter
import utilities

import threading
import time

DEVICE_IP_GLASS = '192.168.17.180'

MAX_RETRY_ATTEMPT = 3


def get_notification_url():
    return f'http://{DEVICE_IP_GLASS}:8080/notifiers/12/'


def get_display_url():
    return f'http://{DEVICE_IP_GLASS}:8080/displays/10/'


def get_touch_bar_url():
    return f'http://{DEVICE_IP_GLASS}:8080/touch/13'


def send_notification_data(notification):
    attempt = 0
    success = False
    while not success and attempt < MAX_RETRY_ATTEMPT:
        success = utilities.send_request(get_notification_url(), notification)
        attempt += 1

        if not success and attempt < MAX_RETRY_ATTEMPT:
            utilities.sleep_seconds(0.8)

    return success


def clear_notification_data():
    send_notification_data(display_formatter.get_empty_notification())


def is_not_blank(string):
    return bool(string and string.strip())


def send_reading_passage(passage):
    display_data = display_formatter.get_display_passage(passage)

    attempt = 0
    success = False
    while not success and attempt < MAX_RETRY_ATTEMPT:
        success = utilities.send_request(get_display_url(), display_data)
        attempt += 1

        if not success and attempt < MAX_RETRY_ATTEMPT:
            utilities.sleep_seconds(0.8)

    return success


def clear_reading_passage():
    send_reading_passage({"id": 0, "title": "", "content": ""})


# handle scrolling

def scroll(down):
    print(f'scroll:: down:{down}')
    if down:
        utilities.send_request(get_touch_bar_url(), {'type': 'ONE_FINGER_SWIPE_DOWN'})
    else:
        utilities.send_request(get_touch_bar_url(), {'type': 'ONE_FINGER_SWIPE_UP'})


def scroll_threaded(down):
    threading.Thread(target=scroll, args=(down,)).start()


def scroll_up():
    print('scroll_up')
    return utilities.send_request(get_touch_bar_url(), {'type': 'ONE_FINGER_SWIPE_UP'})
