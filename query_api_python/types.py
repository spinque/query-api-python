import json

from enum import Enum
from typing import Union, List, Tuple


class ApiAuthenticationConfig:

    def __init__(self, _authentication_config: dict):
        self.auth_server: str = _authentication_config['authServer'] \
            if 'authServer' in _authentication_config.keys() else 'login.spinque.com'
        self.clientId: str = _authentication_config['clientId'] if 'clientId' in _authentication_config.keys() else None
        self.clientSecret: str = \
            _authentication_config['clientSecret'] if 'clientSecret' in _authentication_config.keys() else None

    def to_dict(self) -> dict:
        return {
            'authServer': self.auth_server,
            'clientId': self.clientId,
            'clientSecret': self.clientSecret
        }


class ApiConfig:
    def __init__(self, _api_config):
        self.base_url: str = \
            _api_config['baseUrl'] if 'baseUrl' in _api_config.keys() else 'https://rest.spinque.com/'
        self.version: str = _api_config['version'] if 'version' in _api_config.keys() else '4'
        self.workspace: Union[str, None] = _api_config['workspace'] if 'workspace' in _api_config.keys() else None
        self.api: Union[str, None] = _api_config['api'] if 'api' in _api_config.keys() else None
        self.config: str = _api_config['version'] if 'version' in _api_config.keys() else 'default'
        self.authentication: Union[ApiAuthenticationConfig, None] = \
            ApiAuthenticationConfig(_api_config['authentication']) if 'authentication' in _api_config.keys() else None

    def __str__(self) -> str:
        return json.dumps({
            'baseUrl': self.base_url,
            'version': self.version,
            'workspace': self.workspace,
            'api': self.api,
            'config': self.config,
            'authentication': self.authentication.to_dict() if self.authentication is not None else None
        })


class Query:

    def __init__(self, endpoint: str, parameters: List[Tuple[str, str]]):
        self.endpoint = endpoint
        self.parameters = parameters


class RequestType(Enum):
    RESULTS = 1
    STATISTICS = 2

    def __str__(self) -> str:
        return 'results' if self.name == 'RESULTS' else 'statistics'


class RequestOptionsFormat(Enum):
    JSON = 1
    XML = 2
    RDF = 3
    CSV = 4
    XLSX = 5
