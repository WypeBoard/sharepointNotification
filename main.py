import logging
import logging.config
import time

import schedule as schedule

import Settings
from Sharepoint import Sharepoint
from connector import SQLite


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
    schedule.every(cfg.sharepoint_notifikation.schedule_interval).seconds.do(job_func=critical_scheduler.main)

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    main()
