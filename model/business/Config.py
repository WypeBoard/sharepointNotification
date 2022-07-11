from dataclasses import dataclass, field


@dataclass
class Sharepoint:
    baseurl: str
    view_name: str
    schedule_interval: int
    re_notifikation_schedule: str
    terminal_fields: list[str] = field(default_factory=list)
    toast_fields: list[str] = field(default_factory=list)
    fields: list[str] = field(default_factory=list, init=False)

    def __post_init__(self):
        self.fields = list(set(self.terminal_fields + self.toast_fields))

@dataclass
class Config:
    sharepoint: Sharepoint
