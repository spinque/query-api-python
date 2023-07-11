import json
import requests

from query_api_python.types import ApiConfig, Query, RequestOptions, RequestType
from query_api_python.utils import url_from_queries
from query_api_python.exceptions import EndpointNotFoundError, ServerError, UnauthorizedError, UnknownError
from typing import Union, List


class Api:

    def __init__(self, _api_config: str):
        self.api_config = ApiConfig(json.loads(_api_config))

    def fetch(self,
              queries: Union[Query, List[Query]],
              options: RequestOptions = RequestOptions(),
              result_type: RequestType = RequestType.RESULTS
              ):
        url = url_from_queries(config=self.api_config, queries=queries, request_type=result_type)
        r = requests.get(url, params=options.__dict__)
        return response_handler(r)


def response_handler(response: requests.models.Response):
    match response.status_code:
        case 200:
            return response.json()
        case 401:
            raise UnauthorizedError(response.text, 401)
        case 400:
            if response.json()['message'].startswith('no endpoint'):
                raise EndpointNotFoundError(response.text, 400)
            raise UnknownError(response.text, 400)
        case 500:
            raise ServerError(response.text, 500)
        case default:
            raise UnknownError(response.text, default)
