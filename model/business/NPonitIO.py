from dataclasses import dataclass, field


@dataclass
class NPointIO:
    version: str = field()
    changelog: str = field()
