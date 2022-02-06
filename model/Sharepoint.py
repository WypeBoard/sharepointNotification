from requests_ntlm import HttpNtlmAuth
from shareplum.site import Version, Site

class Sharepoint:

    def __init__(self, config: Config = None):
        if config is None:
            config = init_config()
        self.cred = HttpNtlmAuth(config.sharepoint.username, config.sharepoint.password)
        self.case_view = config.sharepoint.export_case
        self.critical_case_view = config.sharepoint_notifikation.critical_cases
        self.site = Site(config.sharepoint.baseurl, version=Version.v365, auth=self.cred)

    def get_critical_case_view(self) -> list:
        return self.site.List('Cases').get_list_items(view_name=self.critical_case_view)
