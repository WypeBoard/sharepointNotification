from model.business.Changelog import Changelog
from model.business.NotificationGrouping import NotificationGrouping
from util import TimeFactory


class CLI:

    def display_change_log(self, changelog: Changelog) -> None:
        if not changelog.logs:
            print('Application is up-to-date')
            return
        for change in changelog.logs:
            print(f'{change.version}: {change.message}')

    def display_open_cases(self, cases: NotificationGrouping) -> None:
        raise NotImplementedError()

    def display_empty_view(self) -> None:
        print(f'View is currently empty')

    def display_current_time(self) -> None:
        print(f'{TimeFactory.get_datetime()}')



