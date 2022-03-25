import time

from win10toast import ToastNotifier

from model.business.NotificationGrouping import NotificationGrouping


def __create_toast(title: str, message: str) -> ToastNotifier:
    toaster = ToastNotifier()
    toaster.show_toast(title=title, msg=message, icon_path=None, duration=5, threaded=True)
    return toaster


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
