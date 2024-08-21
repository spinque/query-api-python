from spinque_query_api.types import Query, RequestType
from typing import List, Union
from urllib import parse


def path_from_queries(queries: List[Query]) -> str:
    return join([path_from_query(q) for q in queries])


def path_from_query(query: Query) -> str:
    parts = ['e', query.endpoint]
    if query.parameters:
        for name, value in query.parameters:
            parts += ['p', parse.quote(name), parse.quote(value)]
    return join(parts)


def url_from_queries(base_url, version, workspace, api, config, queries: Union[Query, List[Query]],
                     request_type: RequestType = RequestType.RESULTS) -> str:
    if not isinstance(queries, list):
        queries = [queries]

    # Construct base URL containing Spinque version and workspace
    url = base_url
    if not url.endswith('/'):
        url += '/'
    url += join([version, workspace, 'api', api])

    # Add the path represented by the Query objects and request type
    url += '/' + join([path_from_queries(queries), str(request_type)])

    # Add config if provided
    if config:
        url += f'?config={config}'

    return url


def join(segments: List[str]) -> str:
    segments = [seg.strip('/') if i > 0 else seg.rstrip('/') for i, seg in enumerate(segments)]
    result = []
    for seg in segments:
        for s in seg.split('/'):
            if s == '.':
                continue
            elif s == '..':
                result.pop()
                continue
            else:
                result.append(s)
    return '/'.join(result)
