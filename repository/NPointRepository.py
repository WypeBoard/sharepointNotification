from connector.RequestConnector import RequestConnector
from model import Constants
from model.business.NPonitIO import NPointIO, ChangelogRevision


def get_npoint_data() -> NPointIO:
    request = RequestConnector(F'https://api.npoint.io/{Constants.NPOINT_IO_ID}')
    response = request.get()
    json_response = response.json()
    changelog = []
    for change in json_response['changes']:
        changelog.append(ChangelogRevision(version=change['version'], message=change['changelog']))
    return NPointIO(changelog)
