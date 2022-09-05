import math

from model.business.CaseGrouping import CaseGrouping
from model.physical.Notification import Notification

from util import StringUtil, TimeFactory

TAG = 'tag'


class CliTable:

    def __init__(self, cases: CaseGrouping, fields: list[str]):
        self.new_cases = cases.new_entries
        self.returned_cases = cases.reopened_entries
        self.open_cases = cases.ui_entries
        self.fields = fields
        self.add_tag = False

        self.maximum_width = self.calculate_column_width()

    def calculate_column_width(self) -> dict[str, int]:
        column_width = {}
        for field in self.fields:
            column_width[field] = len(field)

        for case in list(self.new_cases + self.returned_cases + self.open_cases):
            for field in self.fields:
                case_field = StringUtil.parse_to_string(case.extra_fields[field])
                column_width[field] = max(len(case_field), column_width[field])
        if len(self.new_cases) + len(self.returned_cases) > 0:
            self.add_tag = True
            column_width[TAG] = 1
        else:
            self.add_tag = False
        return column_width

    def get_ui_length(self) -> int:
        return sum(self.maximum_width.values()) + (2 * len(self.maximum_width.keys())) + len(self.maximum_width.keys()) + 1

    def _seperator_line(self):
        number_of_chars = self.get_ui_length()
        print("#" * number_of_chars)

    def print(self):
        self._seperator_line()
        self._print_timestamp()
        self._seperator_line()
        if len(self.new_cases) + len(self.returned_cases) + len(self.open_cases) > 0:
            self._print_content()
        else:
            self._print_empty()

    def _print_timestamp(self):
        number_of_chars = self.get_ui_length() - 4
        print('# ', end='')
        print(f'{TimeFactory.get_gui_datetime()}'.center(number_of_chars), end='')
        print(' #')

    def _print_content(self):
        self._print_header()
        if self.new_cases:
            self._seperator_line()
            self._print_cases(self.new_cases, 'N')
        if self.returned_cases:
            self._seperator_line()
            self._print_cases(self.returned_cases, 'R')
        if self.open_cases:
            self._seperator_line()
            self._print_cases(self.open_cases)
        self._seperator_line()

    def _print_empty(self):
        number_of_chars = self.get_ui_length() - 4
        print('# ', end='')
        print(f'The view is currently empty'.center(number_of_chars), end='')
        print(' #',)
        self._seperator_line()

    def _print_header(self):
        if self.add_tag:
            print('#   ', end='')
        for field in self.fields:
            print('#', end=' ')
            print(f'{field}'.rjust(self.maximum_width[field]), end=' ')
        print('#')

    def _print_cases(self, cases: list[Notification], tag_text: str = ' ') -> None:
        for case in cases:
            if self.add_tag:
                print('#', end=' ')
                print(f'{tag_text}', end=' ')
            for field in self.fields:
                print('#', end=' ')
                print(f'{case.extra_fields[field]}'.rjust(self.maximum_width[field]), end=' ')
            print('#')
