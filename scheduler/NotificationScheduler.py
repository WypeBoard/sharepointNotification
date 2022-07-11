from model.business.CaseGrouping import CaseGrouping
from model.business.Config import Config
from service import NotificationService, SharepointService, ToastService
from util.UI import UI


def main(ui: UI, cfg: Config) -> None:
    # Fetch data
    open_cases = SharepointService.get_cases_from_notification_view(cfg=cfg)
    db_cases = NotificationService.get_all_entities()

    # Grouping of data
    grouping = CaseGrouping(open_cases, db_cases)

    # print grouping
    ui.display_notifications(grouping, cfg.sharepoint.terminal_fields)

    # Toast
    if grouping.get_toast_count != 0:
        toast = ToastService.create_toast(grouping, cfg)
        ToastService.wait_for_thread_to_close(toast)
    NotificationService.update_and_persist(grouping, cfg)
