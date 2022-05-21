# coding=utf-8


import utilities
import device_driver
import display_formatter

NOTIFICATION_DURATION_MILLIS = 8000
CONSECUTIVE_REQUEST_GAP_SECONDS = 10

TRAINING_NOTIFICATIONS = [
    {
        "id": 1,
        "iconColor": "#ff00ff00",
        "iconName": "battery50",
        "appName": "Battery",
        "title": "Power is low",
        "message": "Please recharge before 5% left",
    },
    {
        "id": 2,
        "iconColor": "#ff4285f4",
        "iconName": "acc",
        "appName": "Contact",
        "title": "Details have updated",
        "message": "Please refresh app to reload",
    },
    {
        "id": 3,
        "iconColor": "#ff888888",
        "iconName": "settings",
        "appName": "Settings",
        "title": "WiFi has deactivated",
        "message": "Trying to connect with internet",
    },
]

TRAINING_PASSAGES = [
    {
        "id": 1,
        "title": "Lorem ipsum",
        "content": "Lorem ipsum is a pseudo-Latin text used in web design, typography, layout, and printing in place of English to emphasise design elements over content. It's also called placeholder (or filler) text. It's a convenient tool for mock-ups. It helps to outline the visual elements of a document or presentation, eg typography, font, or layout. "
    },
    {
        "id": 2,
        "title": "The Grasshopper",
        "content": """A grasshopper spent the summer hopping about in the sun and singing to his heart's content. One day, an ant went hurrying by, looking very hot and weary. \n
\"Why are you working on such a lovely day?\" said the grasshopper. \n
\"I'm collecting food for the winter,\" said the ant, \"and I suggest you do the same.\" And off she went, helping the other ants to carry food to their store. The grasshopper carried on hopping and singing. \n\n\n\n\n\n
When winter came the ground was covered with snow. The grasshopper had no food and was hungry. So he went to the ants and asked for food. \n
\"What did you do all summer when we were working to collect our food?\" said one of the ants.\n
\"I was busy hopping and singing,\" said the grasshopper.\n
\"Well,\" said the ant, \"if you hop and sing all summer, and do no work, then you must starve in the winter.\""""
    },

]

notification_count = 0


def display_next_training_notification():
    global notification_count

    if notification_count >= len(TRAINING_NOTIFICATIONS):
        notification_count = 0

    notification = TRAINING_NOTIFICATIONS[notification_count].copy()

    device_driver.send_notification_data(
        display_formatter.get_notification(notification, 0, NOTIFICATION_DURATION_MILLIS))

    notification_count += 1

    utilities.sleep_seconds(CONSECUTIVE_REQUEST_GAP_SECONDS)


passage_count = 0


def display_next_training_passage():
    global passage_count

    if passage_count >= len(TRAINING_PASSAGES):
        passage_count = 0

    device_driver.send_reading_passage(TRAINING_PASSAGES[passage_count])

    passage_count += 1

    utilities.sleep_seconds(CONSECUTIVE_REQUEST_GAP_SECONDS / 2)


# send scroll up event
device_driver.scroll(False)

_res = ''
while _res != 'x':
    _res = input(
        "Continue? (n = notification, p = passage, d = swipe down, u = swipe up, x = exit)")

    if _res == 'n':
        display_next_training_notification()
    elif _res == 'p':
        display_next_training_passage()
    elif _res == 'd':
        device_driver.scroll(True)
    elif _res == 'u':
        device_driver.scroll(False)
    else:
        device_driver.clear_reading_passage()

device_driver.clear_reading_passage()
device_driver.clear_notification_data()
