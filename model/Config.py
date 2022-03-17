from dataclasses import dataclass


@dataclass
class Sharepoint:
    baseurl: str
    critical_cases: str
    schedule_interval: int
    re_notifikation_schedule: str


@dataclass
class Config:
    sharepoint: Sharepoint
