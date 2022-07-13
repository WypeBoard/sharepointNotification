from typing import Protocol

from model.business.CaseGrouping import CaseGrouping
from model.business.Changelog import Changelog


class UI(Protocol):

    def display_change_log(self, changelog: Changelog) -> None:
        raise NotImplementedError()

    def display_notifications(self, grouping: CaseGrouping, config: list[str]):
        raise NotImplementedError()
