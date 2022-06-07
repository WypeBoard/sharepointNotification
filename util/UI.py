from typing import Protocol

from model.business.Changelog import Changelog
from model.business.NotificationGrouping import NotificationGrouping


class UI(Protocol):

    def display_change_log(self, changelog: Changelog) -> None:
        raise NotImplementedError()

    def display_open_cases(self, cases: NotificationGrouping) -> None:
        raise NotImplementedError()

    def display_empty_view(self) -> None:
        raise NotImplementedError()

    def display_current_time(self) -> None:
        raise NotImplementedError()
