import requests

from spinque_query_api.types import ApiConfig, Query, RequestType
from spinque_query_api.utils import url_from_queries
from spinque_query_api.exceptions import EndpointNotFoundError, ServerError, UnauthorizedError, UnknownError
from spinque_query_api.authentication import Authentication
from typing import Union, List


class Api:

    def __init__(self, _api_config: dict):
        self.api_config = ApiConfig(_api_config)
        self.authentication = None
        if self.api_config.authentication is not None:
            self.authentication = Authentication(
                name=self.api_config.authentication.name,
                auth_server=self.api_config.authentication.auth_server,
                client_id=self.api_config.authentication.clientId,
                client_secret=self.api_config.authentication.clientSecret,
                base_url=self.api_config.base_url,
            )

    def fetch(self,
              queries: Union[Query, List[Query]],
              options=None,
              result_type: RequestType = RequestType.RESULTS
              ) -> dict:
        if options is None:
            options = dict()
        headers = {}
        if self.authentication:
            token, expires = self.authentication.get_access_token()
            headers['Authorization'] = f'Bearer {token}'

        url = url_from_queries(config=self.api_config, queries=queries, request_type=result_type)
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
