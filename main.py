import logging
import logging.config
import time

import schedule as schedule

from model.business import Settings
from model.business.Sharepoint import Sharepoint
from connector import SQLite
from scheduler import NotificationScheduler
from service import NPointService
from util.cli.Cli import CLI


def logging_setup() -> logging.Logger:
    logging.config.fileConfig('logging.conf')
    return logging.getLogger('root')


def main():
    logger = logging_setup()

    logger.debug(f'Fetching settings')
    cfg = Settings.create_and_get_config()
    cli = CLI()

    logger.debug(f'Create local database if needed')
    SQLite.create_database()

    logger.debug(f'Ensuring sharepoint connection')
    Sharepoint(cfg)

    logger.debug(f'Checking if newer version exists')
    #NPointService.check_for_newer_version(cli)

    logger.debug(f'Setting up schedules')
    schedule.every(cfg.sharepoint.schedule_interval).seconds.do(NotificationScheduler.main, cli, cfg)
    NotificationScheduler.main(cli, cfg)
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
