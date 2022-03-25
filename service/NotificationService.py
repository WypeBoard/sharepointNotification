from datetime import datetime
from typing import List

import croniter

from model.business.NotificationGrouping import NotificationGrouping
from model.business.Settings import Settings
from model.enum.NotificationStatus import NotificationStatus
from model.physical.Notification import Notification
from repository import NotificationRepository


def get_all_entities() -> List[Notification]:
    return NotificationRepository.get_all_entities()


def persist(notification: Notification) -> Notification:
    return NotificationRepository.persist_entity(notification)


def map_sharepoint_to_notification(raw_cases: List[dict]) -> List[Notification]:
    res = []
    for sharepoint_case in raw_cases:
        res.append(Notification.map_from_sharepoint(sharepoint_case))
    return res


def db_cases_to_update(db_cases: List[Notification], grouping: NotificationGrouping) -> List[Notification]:
    closed_db_cases = []
    for db_case in db_cases:
        if db_case.status == NotificationStatus.CLOSED:
            continue
        if db_case in grouping.get_all_notifications():
            continue
        db_case.status = NotificationStatus.CLOSED
        closed_db_cases.append(db_case)
    return closed_db_cases


def calculate_next_notification(re_notifikation_schedule):
    cron = croniter.croniter(re_notifikation_schedule)
    return datetime.fromtimestamp(next(cron))


def update_cases_to_open(grouping: NotificationGrouping) -> List[Notification]:
    cfg = Settings()
    next_notification = calculate_next_notification(cfg.get_config().sharepoint.re_notifikation_schedule)
    for notification in grouping.get_all_notifications():
        notification.status = NotificationStatus.OPEN
        notification.next_notification = next_notification
    return grouping.get_all_notifications()


def update_and_persist(db_cases: List[Notification], grouping: NotificationGrouping):
    persist_notifications = []
    # Any in db_cases not in cases_to_toast -> closed!
    persist_notifications += db_cases_to_update(db_cases, grouping)
    # all in cases_to_toast -> open!
    persist_notifications += update_cases_to_open(grouping)
    # persist
    for notification in persist_notifications:
        persist(notification)
