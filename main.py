import logging
import logging.config
import time

import schedule as schedule

from model import Settings
from model.Sharepoint import Sharepoint
from connector import SQLite
from scheduler import NotificationScheduler


def logging_setup():
    logging.config.fileConfig('logging.conf')


def main():
    logging_setup()
    logger = logging.getLogger('root')

    logger.info(f'Fetching settings')
    cfg = Settings.create_and_get_config()

    logger.info(f'Create local database if needed')
    SQLite.create_database()

    logger.info(f'Ensuring sharepoint connection')
    Sharepoint(cfg)

    logger.info(f'Setting up schedules')
    schedule.every(cfg.sharepoint.schedule_interval).seconds.do(job_func=NotificationScheduler.main)
    NotificationScheduler.main()
    while True:
        n = schedule.idle_seconds()
        if n is None:
            # No more jobs
            break
        elif n > 0:
            # sleep for n seconds, for when next schedule run
            time.sleep(n)
        schedule.run_pending()


if __name__ == '__main__':
    main()
