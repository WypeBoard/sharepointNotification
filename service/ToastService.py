import time
from typing import List

from win10toast import ToastNotifier

from model.NotificationGrouping import NotificationGrouping
from model.physical.Notification import Notification


def __create_toast(title: str, message: str) -> ToastNotifier:
    toaster = ToastNotifier()
    toaster.show_toast(title=title, msg=message, icon_path=None, duration=5, threaded=True)
    return toaster


def _get_case_titles(cases: List[Notification]) -> str:
    description_string = ''
    for case in cases:
        description_string += f'{case.case_id} {case.case_title}\n'
    return description_string


def _get_title(cases_to_toast):
    return f'{len(cases_to_toast)} number of Priority cases'


def wait_for_thread_to_close(toast: ToastNotifier):
    if toast is None:
        return
    while toast.notification_active():
        time.sleep(0.1)


def create_toast(grouping: NotificationGrouping) -> ToastNotifier:
    if grouping.get_notification_number() == 0:
        return None
    title = grouping.get_toast_title()
    description = grouping.get_toast_description()
    return __create_toast(title, description)
