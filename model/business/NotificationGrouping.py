from typing import List

from model.enum.NotificationStatus import NotificationStatus
from model.physical.Notification import Notification
from util import TimeFactory


def is_in_db_list(notify: Notification, db_notifications: List[Notification]) -> bool:
    db_ids = [db_notify.case_id for db_notify in db_notifications]
    return notify.case_id in db_ids


def is_not_in_db_list(notify: Notification, db_notifications: List[Notification]) -> bool:
    return not is_in_db_list(notify, db_notifications)


def get_all_cases_exceeding_notification_limit(sharepoint_notifications: List[Notification],
                                               db_notifications: List[Notification],
                                               status: NotificationStatus) -> List[Notification]:
    data = []
    for db_case in db_notifications:
        if db_case.status != status:
            continue
        if is_not_in_db_list(db_case, sharepoint_notifications):
            continue
        if db_case.next_notification <= TimeFactory.get_datetime():
            data.append(db_case)
    return data


class NotificationGrouping:

    def __init__(self, sharepoint_notifications: List[Notification], db_notifications: List[Notification]):
        self.new_notifications = [notify for notify in sharepoint_notifications if
                                  is_not_in_db_list(notify, db_notifications)]
        self.re_opened_notifications = get_all_cases_exceeding_notification_limit(sharepoint_notifications,
                                                                                  db_notifications,
                                                                                  NotificationStatus.OPEN)
        self.closed_notifications = get_all_cases_exceeding_notification_limit(sharepoint_notifications,
                                                                               db_notifications,
                                                                               NotificationStatus.CLOSED)
        self.all_notifications = set(self.new_notifications + self.re_opened_notifications + self.closed_notifications)

    def get_all_notifications(self):
        return self.all_notifications

    def get_notification_number(self):
        return len(self.all_notifications)

    def get_toast_description(self):
        toast_msg = ''
        for toast in self.all_notifications:
            toast_msg += f'{toast.case_id} {toast.case_title}\n'
        return toast_msg

    def get_toast_title(self):
        return f'{self.get_notification_number()} number of cases in view'

