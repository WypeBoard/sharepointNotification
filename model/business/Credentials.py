import keyring
from keyring.credentials import SimpleCredential
from requests_ntlm import HttpNtlmAuth


class Credentials:

    def __init__(self, service_group: str):
        temp_credentials = keyring.get_credential(service_name=service_group, username=None)
        if temp_credentials is None:
            username = input(f'Please type in your Username, this should include <domain>\<username>: ')
            password = input(f'Please type or paste your Toolkit password here: ')
            self.__set_password_in_keyring(service_group, username, password)
            temp_credentials = SimpleCredential(username, password)
        self.credentials = temp_credentials

    @staticmethod
    def __set_password_in_keyring(service_group: str, username: str, password: str):
        keyring.set_password(service_group, username, password)

    def get_auth_creadentials(self):
        return HttpNtlmAuth(username=self.credentials.username, password=self.credentials.password)
