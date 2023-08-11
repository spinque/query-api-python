from spinque_query_api.types import ApiConfig, Query, RequestType
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


def url_from_queries(config: ApiConfig,
                     queries: Union[Query, List[Query]],
                     request_type: RequestType = RequestType.RESULTS
                     ) -> str:
    if not type(queries) == list:
        queries = [queries]
    if not config.base_url:
        raise ValueError('Base URL missing')
    if not config.version:
        raise ValueError('Version missing')
    if not config.workspace:
        raise ValueError('Workspace missing')
    if not config.api:
        raise ValueError('API name missing')

    # Construct base URL containing Spinque version and workspace
    url = config.base_url
    if not url.endswith('/'):
        url += '/'
    url += join([config.version, config.workspace, 'api', config.api])

    # Add the path represented by the Query objects and request type
    url += '/' + join([path_from_queries(queries), str(request_type)])

    # Add config if provided
    if config.config:
        url += f'?config={config.config}'

    return url


def join(segments: List[str]) -> str:
    segments = [seg.strip('/') if i > 0 else seg.rstrip('/') for i, seg in enumerate(segments)]
    result = []
    for seg in segments:
        for s in seg.split('/'):
            match s:
                case '.':
                    continue
                case '..':
                    result.pop()
                    continue
                case _:
                    result.append(s)
    return '/'.join(result)
