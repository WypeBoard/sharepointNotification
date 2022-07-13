from dataclasses import dataclass, field


@dataclass
class ChangelogRevision:
    message: str = field()
    version: str = field()
    major_version: int = field(init=False)
    minor_version: int = field(init=False)
    hotfix_version: int = field(init=False)

    def __post_init__(self):
        self.major_version, self.minor_version, self.hotfix_version = [int(x) for x in self.version.split('.')]

    def __gt__(self, other):
        if self.major_version > other.major_version:
            return True
        if self.minor_version > other.minor_version:
            return True
        return self.hotfix_version > other.hotfix_version

    def __eq__(self, other):
        return (
                self.major_version == other.major_version and
                self.minor_version == other.minor_version and
                self.hotfix_version == other.hotfix_version
        )


@dataclass
class NPointIO:
    changelog: list[ChangelogRevision] = field(default_factory=list)
