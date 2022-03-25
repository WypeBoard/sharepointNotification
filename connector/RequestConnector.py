import requests


class RequestConnector:

    def __init__(self, url: str):
        self.url: str = url
        self.response = None

    def get(self):
        self.response = requests.get(self.url)
        return self.response

    def get_json(self):
        return self.response.json()
