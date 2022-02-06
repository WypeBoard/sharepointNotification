from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import List
from uuid import uuid4

from util import TimeFactory


@dataclass
class BaseEntity(ABC):
    id: str = field()
    oprettet: datetime = field()
    oprettet_af: str = field()
    aendret: datetime = field()
    aendret_af: str = field()

    @abstractmethod
    def map_from_db(self, db_entity: List):
        """ Mapping data from db to the class representation """

    def create_new_db_entity(self):
        self.id = str(uuid4())
        self.oprettet = TimeFactory.get_datetime()
        self.oprettet_af = 'SYSTEM'
        self.aendret = TimeFactory.get_datetime()
        self.aendret_af = 'SYSTEM'

    def update_db_entity(self):
        self.aendret = TimeFactory.get_datetime()
        self.aendret_af = 'SYSTEM'
