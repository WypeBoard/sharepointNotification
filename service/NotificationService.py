from datetime import datetime
from typing import List

import croniter

from model.business.CaseGrouping import CaseGrouping
from model.business.Config import Config
from model.enum.NotificationStatus import NotificationStatus
from model.physical.Notification import Notification
from repository import NotificationRepository


def get_all_entities() -> List[Notification]:
    return NotificationRepository.get_all_entities()


def persist(notification: Notification) -> Notification:
    return NotificationRepository.persist_entity(notification)


def map_sharepoint_to_notification(raw_cases: List[dict], fields: list[str]) -> List[Notification]:
    res = []
    for sharepoint_case in raw_cases:
        res.append(Notification.map_from_sharepoint(sharepoint_case, fields))
    return res


def calculate_next_notification(re_notifikation_schedule):
    cron = croniter.croniter(re_notifikation_schedule)
    return datetime.fromtimestamp(next(cron))


def mark_and_persist_closed_cases(grouping: CaseGrouping) -> None:
    """
    Simply as we know all closed cases
    We only know that these are closed due to the fact that all entries has id.
    :param grouping: Grouping of all Sharepoint and Db cases.
    :return: None
    """
    for case in grouping.closed_entries:
        case.close()
        persist(case)


def mark_and_persist_open_cases(grouping: CaseGrouping, cfg: Config) -> None:
    """
    All entries are open, and needs to be marked as such.
    NextNotification also needs to be updated.

    Unless we do some grouping we do not know if the entry is known in DB.
    Keeping this simple and letting the Repository handle that
    :param cfg:
    :param grouping: Grouping of all Sharepoint and Db cases.
    :return: None
    """
    next_notification = calculate_next_notification(cfg.sharepoint.re_notifikation_schedule)
    for case in grouping.open_cases:
        case.open(next_notification)
        persist(case)


def update_and_persist(grouping: CaseGrouping, cfg: Config) -> None:
    """
    Close all Cases no longer in Sharepoint view
    All open cases update next entity and persist
    :param cfg:
    :param grouping: Grouping of all Sharepoint and Db cases.
    :return: None
    """
    # Update db with closed cases!
    mark_and_persist_closed_cases(grouping)

    # Update db with open cases!
    mark_and_persist_open_cases(grouping, cfg)
