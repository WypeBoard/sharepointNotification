import logging
from typing import List

from model.NotificationGrouping import NotificationGrouping
from model.physical.Notification import Notification
from service import NotificationService, SharepointService, ToastService


def get_sharepoint_notification_description(sharepoint_notifications: List[Notification]):
    log_string = '\n'
    for notification in sharepoint_notifications:
        log_string += notification.case_id + ' ' + notification.case_title + '\n'
    return log_string


def main():
    # TODO: Better name?
    logger = logging.getLogger('root')
    logger.debug(f'Critical Scheduler running..')

    logger.debug(f'fetching sharepoint view data')
    sharepoint_notifications = SharepointService.get_cases_from_notification_view()
    if len(sharepoint_notifications) == 0:
        logger.info(f'The view is currently empty\n')
        return

    logger.info(f'There is currently {len(sharepoint_notifications)} cases in the view')
    logger.info(f'{get_sharepoint_notification_description(sharepoint_notifications)}')

    logger.debug(f'fetching database entries')
    db_notifications = NotificationService.get_all_entities()
    grouping = NotificationGrouping(sharepoint_notifications, db_notifications)
    logger.info(f'{grouping.get_notification_number()} out of {len(sharepoint_notifications)} is being reported\n')
    if grouping.get_notification_number() != 0:
        toast = ToastService.create_toast(grouping)
        NotificationService.update_and_persist(db_notifications, grouping)
        ToastService.wait_for_thread_to_close(toast)