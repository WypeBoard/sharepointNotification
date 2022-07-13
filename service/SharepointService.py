from typing import List

from model.business.Config import Config
from model.business.Sharepoint import Sharepoint
from model.physical.Notification import Notification
from service import NotificationService


def get_cases_from_notification_view(cfg: Config) -> List[Notification]:
    sharepoint = Sharepoint(config=cfg)
    raw_cases = sharepoint.get_critical_case_view()
    return NotificationService.map_sharepoint_to_notification(raw_cases, cfg.sharepoint.fields)
