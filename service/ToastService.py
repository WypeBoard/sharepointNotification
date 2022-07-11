import time

from win10toast import ToastNotifier

from model.business.CaseGrouping import CaseGrouping
from model.business.Config import Config
from model.physical.Notification import Notification


def __create_toast(title: str, message: str) -> ToastNotifier:
    toaster = ToastNotifier()
    toaster.show_toast(title=title, msg=message, icon_path=None, duration=5, threaded=True)
    return toaster


def wait_for_thread_to_close(toast: ToastNotifier):
    if toast is None:
        return
    while toast.notification_active():
        time.sleep(0.1)


def __compute_title(count: int) -> str:
    return f'{count} number of cases in view'


def __compute_toast_fields(case: Notification, toast_fields: list[str], prepend: str | None) -> str:
    if prepend:
        description = prepend + ' '
    else:
        description = ''
    for field in toast_fields:
        description += f'{case.extra_fields[field]} '
    return description[:45]


def __compute_description(grouping: CaseGrouping, toast_fields: list[str]) -> str:
    toast_msg = ''
    for toast in grouping.new_entries:
        toast_msg += __compute_toast_fields(toast, toast_fields, '[N]')
    for toast in grouping.reopened_entries:
        toast_msg += __compute_toast_fields(toast, toast_fields, '[R]')
    for toast in grouping.toast_entries:
        toast_msg += __compute_toast_fields(toast, toast_fields, None)
    return toast_msg


def create_toast(grouping: CaseGrouping, cfg: Config) -> None | ToastNotifier:
    title = __compute_title(grouping.get_toast_count)
    description = __compute_description(grouping, cfg.sharepoint.toast_fields)
    return __create_toast(title, description)
