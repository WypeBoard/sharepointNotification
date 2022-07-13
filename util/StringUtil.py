from datetime import datetime

from util import TimeFactory

EMPTY_STRING = ''


def parse_to_string(param: any) -> str:
    if param is None:
        return EMPTY_STRING
    if type(param) is str:
        return param
    if type(param) is datetime:
        return TimeFactory.to_gui_date(param)
    return EMPTY_STRING
