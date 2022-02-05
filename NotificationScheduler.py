import logging


def main():
    # TODO: Better name?
    logger = logging.getLogger('root')
    logger.debug(f'Critical Scheduler running..')

    logger.debug(f'fetching sharepoint view data')
    raw_sharepoint_cases = SharepointService.get_critical_cases()
    logger.info(f'There is currently {len(raw_sharepoint_cases)} cases in the view')

    logger.debug(f'fetching database entries')
    db_cases = NotificationService.get_all_entities()


