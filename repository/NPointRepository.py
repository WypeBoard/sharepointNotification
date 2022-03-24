from connector.RequestConnector import RequestConnector
from model import Constants
from model.business.NPonitIO import NPointIO


def get_npoint_data() -> NPointIO:
    request = RequestConnector(F'https://api.npoint.io/{Constants.NPOINT_IO_ID}')
    response = request.get()
    json_response = response.json()
    return NPointIO(json_response['version'], json_response['changelog'])
