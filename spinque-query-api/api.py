import requests

from spinque_query_api.types import Query, RequestType
from spinque_query_api.utils import url_from_queries
from spinque_query_api.exceptions import EndpointNotFoundError, ServerError, UnauthorizedError, UnknownError
from spinque_query_api.authentication import Authentication
from typing import Union, List


class Api:

    def __init__(self, workspace, api, base_url='https://rest.spinque.com/', version='4', config='default',
                 authentication: Authentication = None):
        self.workspace = workspace
        self.api = api

        self.base_url = base_url
        self.version = version
        self.config = config
        self.authentication = authentication

    def fetch(self, queries: Union[Query, List[Query]], options=None,
              result_type: RequestType = RequestType.RESULTS) -> dict:
        if options is None:
            options = dict()
        headers = {}
        if self.authentication:
            token, expires = self.authentication.get_access_token()
            headers['Authorization'] = f'Bearer {token}'

        url = url_from_queries(base_url=self.base_url, version=self.version, workspace=self.workspace, api=self.api,
                               config=self.config, queries=queries, request_type=result_type)
        r = requests.get(url, options, headers=headers)
        return response_handler(r)


def response_handler(response: requests.models.Response) -> dict:
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 401:
        raise UnauthorizedError(response.text, 401)
    elif response.status_code == 400:
        if response.json()['message'].startswith('no endpoint'):
            raise EndpointNotFoundError(response.text, 400)
        raise UnknownError(response.text, 400)
    elif response.status_code == 500:
        raise ServerError(response.text, 500)
    else:
        raise UnknownError(response.text)
