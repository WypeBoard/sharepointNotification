from model import Constants
from model.business.Changelog import Changelog, ChangelogVersion
from model.business.NPonitIO import ChangelogRevision
from repository import NPointRepository
from util.UI import UI


def changelog_of_current_version() -> ChangelogRevision:
    return ChangelogRevision(version=Constants.CURRENT_VERSION, message='')


def check_for_newer_version(ui: UI) -> None:
    np_point = NPointRepository.get_npoint_data()
    current_version = changelog_of_current_version()
    newer_versions = Changelog()
    for changelog in np_point.changelog:
        if changelog > current_version:
            newer_versions.logs.append(ChangelogVersion(version=changelog.version, message=changelog.message))
    ui.display_change_log(newer_versions)