from model import Constants
from repository import NPointRepository


def check_for_newer_version() -> None:
    np_point = NPointRepository.get_npoint_data()
    up_to_date = np_point.version == Constants.CURRENT_VERSION
    if not up_to_date:
        print(f'Current version is {Constants.CURRENT_VERSION}, newest version is {np_point.version}')
        # TODO. Det her er ikke specielt godt. Men works for now
        print('***************************')
        print('* Newer version available *')
        print('***************************')
        print('* Changes * ')
        print(np_point.changelog)
        print('\n\n')
