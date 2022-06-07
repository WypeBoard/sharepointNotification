from dataclasses import dataclass, field


@dataclass
class ChangelogVersion:
    version: str = field()
    message: str = field()

@dataclass
class Changelog:
    logs: list[ChangelogVersion] = field(default_factory=list)
