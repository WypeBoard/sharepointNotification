from dataclasses import dataclass, field

from model.enum.NotificationStatus import NotificationStatus
from model.physical.Notification import Notification
from util import TimeFactory


def is_entry_in_collection(case: Notification, case_collection: list[Notification]) -> bool:
    db_ids = [db_notify.case_id for db_notify in case_collection]
    return case.case_id in db_ids


def is_entry_not_in_collection(case: Notification, case_collection: list[Notification]) -> bool:
    return not is_entry_in_collection(case, case_collection)


def is_entry_in_collection_with_status(case: Notification, case_collection: list[Notification], status: NotificationStatus) -> bool:
    collection_ids = [entry.case_id for entry in case_collection if entry.status == status]
    return case.case_id in collection_ids


def is_entry_not_in_collection_with_status(case: Notification, case_collection: list[Notification], status: NotificationStatus) -> bool:
    return not is_entry_in_collection_with_status(case, case_collection, status)


def get_entry_in_collection_with_status(case: Notification, case_collection: list[Notification], status: NotificationStatus) -> Notification | None:
    for c_case in case_collection:
        if c_case.status is not status:
            continue
        if c_case.case_id == case.case_id:
            return c_case
    return None


def get_running_toast_entries(sharepoint_cases: list[Notification],
                              db_cases: list[Notification],
                              status: NotificationStatus) -> list[Notification]:
    data = []
    for case in sharepoint_cases:
        db_case = get_entry_in_collection_with_status(case, db_cases, status)
        if db_case is None:
            continue
        if db_case.next_notification <= TimeFactory.get_datetime():
            data.append(case)
    return data


@dataclass
class CaseGrouping:
    # Raw data
    sharepoint_cases: list[Notification] = field(default_factory=list)
    db_cases: list[Notification] = field(default_factory=list)

    # Calculated data
    new_entries: list[Notification] = field(default_factory=list, init=False)
    reopened_entries: list[Notification] = field(default_factory=list, init=False)

    # UI - Rest (not found in new_entries or reopened_entries)
    ui_entries: list[Notification] = field(default_factory=list, init=False)

    # Toast - running notifications
    toast_entries: list[Notification] = field(default_factory=list, init=False)

    # Used for persisting, populates with db_cases first and adds missing new cases on top
    open_cases: list[Notification] = field(default_factory=list, init=False)
    closed_entries: list[Notification] = field(default_factory=list, init=False)

    def __post_init__(self):
        self.new_entries = self.__compute_new_entries()
        self.reopened_entries = self.__compute_re_opened_closed_cases()
        self.ui_entries = self.__compute_ui_entries()
        self.toast_entries = self.__compute_toast_entries()
        self.open_cases = self.__compute_open_cases()
        self.closed_entries = self.__compute_closed_cases()

    def __compute_new_entries(self) -> list[Notification]:
        return [case for case in self.sharepoint_cases if is_entry_not_in_collection(case, self.db_cases)]

    def __compute_re_opened_closed_cases(self) -> list[Notification]:
        return [case for case in self.sharepoint_cases if is_entry_in_collection_with_status(case, self.db_cases, NotificationStatus.CLOSED)]

    def __compute_ui_entries(self) -> list[Notification]:
        temp_entries = self.sharepoint_cases.copy()
        for case in list(self.new_entries + self.reopened_entries):
            temp_entries.remove(case)
        return temp_entries

    def __compute_toast_entries(self) -> list[Notification]:
        return get_running_toast_entries(self.sharepoint_cases, self.db_cases, NotificationStatus.OPEN)

    def __compute_open_cases(self) -> list[Notification]:
        previously_open_cases = [case for case in self.db_cases if is_entry_in_collection(case, self.sharepoint_cases)]
        newly_open_cases = [case for case in self.sharepoint_cases if is_entry_not_in_collection(case, previously_open_cases)]
        return previously_open_cases + newly_open_cases

    def __compute_closed_cases(self) -> list[Notification]:
        return [case for case in self.db_cases if is_entry_not_in_collection_with_status(case, self.sharepoint_cases, NotificationStatus.OPEN)]

    @property
    def get_toast_count(self) -> int:
        return len(self.new_entries + self.reopened_entries + self.toast_entries)
