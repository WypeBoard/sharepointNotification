from dataclasses import dataclass


@dataclass
class Sharepoint:
    username: str
    password: str
    baseurl: str


@dataclass
class SharepointNotification:
    critical_cases: str
    schedule_interval: int
    re_notifikation_schedule: str


@dataclass
class Config:
    sharepoint: Sharepoint
    sharepoint_notifikation: SharepointNotification
