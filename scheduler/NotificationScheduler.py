import logging
from typing import List

from model.business.NotificationGrouping import NotificationGrouping
from model.physical.Notification import Notification
from service import NotificationService, SharepointService, ToastService
from util.UI import UI


def get_sharepoint_notification_description(sharepoint_notifications: List[Notification]):
    log_string = '\n'
    for notification in sharepoint_notifications:
        log_string += notification.case_id + ' ' + notification.case_title + '\n'
    return log_string


def main(ui: UI):
    logger = logging.getLogger('root')
    logger.debug(f'Critical Scheduler running..')
    ui.display_current_time()

    sharepoint_notifications = SharepointService.get_cases_from_notification_view()
    if len(sharepoint_notifications) == 0:
        ui.display_empty_view()
        return

    logger.debug(f'There is currently {len(sharepoint_notifications)} cases in the view')
    logger.debug(f'{get_sharepoint_notification_description(sharepoint_notifications)}')

    logger.debug(f'fetching database entries')
    db_notifications = NotificationService.get_all_entities()
    grouping = NotificationGrouping(sharepoint_notifications, db_notifications)
    ui.display_open_cases(grouping)

    logger.debug(f'{grouping.get_notification_number()} out of {len(sharepoint_notifications)} is being reported\n')
    if grouping.get_notification_number() != 0:
        toast = ToastService.create_toast(grouping)
        NotificationService.update_and_persist(db_notifications, grouping)
        ToastService.wait_for_thread_to_close(toast)
    ui.display_current_time()
