from dataclasses import dataclass, field
from datetime import datetime

from model.enum.NotificationStatus import NotificationStatus
from model.physical.BaseEntity import BaseEntity
from util import TimeFactory, StringUtil


@dataclass
class Notification(BaseEntity):
    case_id: str = field()
    case_title: str = field()
    status: NotificationStatus = field()
    next_notification: datetime = field()
    extra_fields: dict = field(default_factory=dict)

    def __hash__(self):
        return hash((self.id, self.case_id))

    @classmethod
    def map_from_db(cls, db_entity: tuple):
        return Notification(id=db_entity[0],
                            case_id=db_entity[1],
                            case_title=db_entity[2],
                            status=NotificationStatus[db_entity[3]],
                            next_notification=TimeFactory.from_database_datetime(db_entity[4]),
                            oprettet=TimeFactory.from_database_datetime(db_entity[5]),
                            oprettet_af=db_entity[6],
                            aendret=TimeFactory.from_database_datetime(db_entity[7]),
                            aendret_af=db_entity[8],
                            extra_fields={})

    @classmethod
    def map_from_sharepoint(cls, case: dict, extra_fields: list[str]):
        additional_fields = {x: StringUtil.parse_to_string(case.get(x, '')) for x in extra_fields}
        return Notification(id=None,
                            case_id=case['Case Id'],
                            case_title=case['Title'],
                            status=NotificationStatus.OPEN,
                            next_notification=None,
                            extra_fields=additional_fields,
                            oprettet=None,
                            oprettet_af=None,
                            aendret=None,
                            aendret_af=None)

    def close(self) -> None:
        self.status = NotificationStatus.CLOSED

    def open(self, next_notification) -> None:
        self.status = NotificationStatus.OPEN
        self.next_notification = next_notification
