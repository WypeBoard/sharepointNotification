from configparser import ConfigParser as cp

from model.Config import Sharepoint, Config


def create_and_get_config():
    settings = Settings()
    return settings.get_config()


class Settings:

    def __init__(self, config_path: str = 'config.ini'):
        self._configparser = cp()
        self._configparser.read(config_path)
        self._required_sections = ['sharepoint']
        self._validate_field_population()
        self._cfg = self.__generate_config()

    def get_config(self):
        return self._cfg

    def __get_sharepoint_config(self, section: str) -> Sharepoint:
        baseurl = self._get_property(section, 'baseurl')
        critical_cases = self._get_property(section, 'critical_cases')
        schedule_interval = self._get_int_property_min_value(section, 'schedule_interval', 120)
        re_notifikation_schedule = self._get_property(section, 're_notifikation_schedule')
        return Sharepoint(baseurl=baseurl, critical_cases=critical_cases, schedule_interval=schedule_interval, re_notifikation_schedule=re_notifikation_schedule)

    def __generate_config(self) -> Config:
        return Config(self.__get_sharepoint_config('sharepoint'))

    def _validate_field_population(self) -> None:
        _sections = self._configparser.sections()
        for _section in _sections:
            if _section not in self._required_sections:
                continue
            for _key, _value in self._configparser.items(section=_section):
                self._validate_required_key(_section, _key, _value)

    def _get_property(self, section, key):
        return self._configparser.get(section, key)

    def _get_int_property_min_value(self, section, key, min_value) -> int:
        try:
            temp_int = int(self._get_property(section, key))
            return temp_int if temp_int > min_value else min_value
        except ValueError:
            raise NotImplementedError(f'value for key {key} is not an integer')

    def _validate_required_key(self, _section, _key, _value) -> None:
        if not _value:
            raise NotImplementedError(f'Missing value from {_key}')
