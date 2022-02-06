from typing import List

from model.Sharepoint import Sharepoint
from model.physical.Notification import Notification
from service import NotificationService


def get_cases_from_notification_view() -> List[Notification]:
    sharepoint = Sharepoint()
    raw_cases = sharepoint.get_critical_case_view()
    return NotificationService.map_sharepoint_to_notification(raw_cases)
