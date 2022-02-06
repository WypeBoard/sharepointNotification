from configparser import ConfigParser as cp

from model.Config import Sharepoint, SharepointNotification, Config


def create_and_get_config():
    settings = Settings()
    return settings.get_config()


class Settings:

    def __init__(self, config_path: str = 'config.ini'):
        self._configparser = cp()
        self._configparser.read(config_path)
        self._required_sections = ['sharepoint', 'sharepoint_notification', 'db']
        self._validate_field_population()
        self._cfg = self.__generate_config()

    def get_config(self):
        return self._cfg

    def __get_sharepoint_config(self) -> Sharepoint:
        username = self._get_property('sharepoint', 'username')
        password = self._get_property('sharepoint', 'password')
        baseurl = self._get_property('sharepoint', 'baseurl')
        return Sharepoint(username=username, password=password, baseurl=baseurl)

    def __get_sharepoint_notification_config(self) -> SharepointNotification:
        critical_cases = self._get_property('sharepoint_notification', 'critical_cases')
        schedule_interval = self._get_int_property('sharepoint_notification', 'schedule_interval')
        re_notifikation_schedule = self._get_property('sharepoint_notification', 're_notifikation_schedule')
        return SharepointNotification(critical_cases, schedule_interval, re_notifikation_schedule)

    def __generate_config(self) -> Config:
        share_config = self.__get_sharepoint_config()
        share_notification_config = self.__get_sharepoint_notification_config()
        return Config(share_config, share_notification_config)

    def _validate_field_population(self) -> None:
        _sections = self._configparser.sections()
        for _section in _sections:
            if _section not in self._required_sections:
                continue
            for _key, _value in self._configparser.items(section=_section):
                self._validate_required_key(_section, _key, _value)

    def _get_property(self, section, key):
        return self._configparser.get(section, key)

    def _get_int_property(self, section, key) -> int:
        try:
            return int(self._get_property(section, key))
        except ValueError:
            raise NotImplementedError(f'Værdien i sektionen: {section} med værdien {key} er ikke et hel tal')

    def _validate_required_key(self, _section, _key, _value) -> None:
        if not _value:
            raise NotImplementedError(f'Missing value from {_key}')
