from shareplum.site import Version, Site

from model.business.Config import Config
from model.business.Credentials import Credentials
from model.business.Settings import Settings


def init_config():
    settings = Settings()
    return settings.get_config()


class Sharepoint:

    def __init__(self, config: Config = None):
        if config is None:
            config = init_config()
        cred = Credentials('python_sharepoint_application')
        self.critical_case_view = config.sharepoint.critical_cases
        self.site = Site(config.sharepoint.baseurl, version=Version.v365, auth=cred.get_auth_creadentials())

    def get_critical_case_view(self) -> list:
        return self.site.List('Cases').get_list_items(view_name=self.critical_case_view)
