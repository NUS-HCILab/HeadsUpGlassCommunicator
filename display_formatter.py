# coding=utf-8

## maps data to smart glass supported format

GLASS_NOTIFICATION_TYPE_HEADS_UP = 1


def get_empty_notification():
    return {
        "type": GLASS_NOTIFICATION_TYPE_HEADS_UP,
        "id": -1,
        "title": "",
    }


# notification_data: { "iconColor": <#color> , "iconName":  <app_icon> }
def _get_notification_icon(notification_data):
    if notification_data.get("iconName"):
        print(notification_data.get('iconName'))
        if notification_data.get("iconColor"):
            return f'{notification_data.get("iconColor")} {notification_data.get("iconName")}'
        else:
            return f'#FFFFFFFF {notification_data.get("iconName")}'
    else:
        return ""


def _get_notification_config(notification_data, config):
    if config:  # non-empty config
        return config

    if notification_data.get("config"):
        return notification_data.get("config")

    return ''


def _get_notification_attribute(value):
    if value:
        return value
    else:
        return ''


# notification_data: { "id": <id>, "title": <title>, "message": <message> , "iconColor": <#color> , "iconName":  <app_icon>, "appName": <app_name> }
# all time related data in millis
def get_notification(notification_data, when, duration, config=None):
    return {
        "type": GLASS_NOTIFICATION_TYPE_HEADS_UP,
        "id": _get_notification_attribute(notification_data.get("id")),
        "title": _get_notification_attribute(notification_data.get("title")),
        "message": _get_notification_attribute(notification_data.get("message")),
        "appName": _get_notification_attribute(notification_data.get("appName")),
        "when": when,
        "duration": duration,
        "smallIcon": _get_notification_icon(notification_data),
        "config": _get_notification_config(notification_data, config)
    }


def get_updated_notification_with_reading_passage(notification, notification_config,
                                                  reading_question, when):
    # update when to show notification
    notification.update({"when": when})

    # append the question to the notification_config
    notification_config = "{},{},{},".format(notification_config,
                                             reading_question.get('Header', ''),
                                             reading_question.get('Passage').replace(",", "|"))
    notification.update({"config": notification_config})

    return notification


def get_updated_subsequent_notification(notification, notification_config, when):
    # update when to show notification
    notification.update({"when": when})

    # update config to support no refresh
    notification_config = "{},".format(
        notification_config.replace("PROGRESSIVE_WITH_DISPLAY", "PROGRESSIVE_WITH_NO_REFRESH"))
    notification.update({"config": notification_config})

    return notification


def get_display_passage(passage):
    return {
        "id": passage.get('id', ''),
        "heading": passage.get('title', ''),
        "subheading": '',
        "content": passage.get('content', ''),
    }


def get_display_data_without_refresh(heading, subheading, content=""):
    return {
        "heading": heading,
        "subheading": subheading,
        "content": content,
        "config": "NO_REFRESH"
    }


def get_dummy_display_data():
    return {
        "subheading": "Lorem ipsum is a pseudo-Latin text used in web design, typography, layout, "
                      "and printing in place of English to emphasise design elements over content. "
                      "It's also called placeholder (or filler) text. It's a convenient tool for mock-ups. "
                      "It helps to outline the visual elements of a document or presentation, "
                      "eg typography, font, or layout. Lorem ipsum is mostly a part of a Latin text "
                      "by the classical author and philosopher Cicero. Its words and letters have been "
                      "changed by addition or removal, so to deliberately render its content nonsensical;"
                      " it's not genuine, correct, or comprehensible Latin anymore."
    }
