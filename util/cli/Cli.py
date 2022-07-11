from model.business.CaseGrouping import CaseGrouping
from model.business.Changelog import Changelog

from util.cli.CliTable import CliTable

import os

class CLI:

    def display_change_log(self, changelog: Changelog) -> None:
        if not changelog.logs:
            print('Application is up-to-date')
            return
        print(f'Newer version of the program available')
        for change in changelog.logs:
            print(f'{change.version}: {change.message}')

    def display_notifications(self, grouping: CaseGrouping, display_fields: list[str]):
        print(f'\n\n')
        table = CliTable(grouping, display_fields)
        table.print()


