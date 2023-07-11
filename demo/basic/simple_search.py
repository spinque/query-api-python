import json

from query_api_python import Api, Query, RequestOptions

api = Api(
    json.dumps(
        {
            'workspace': 'playground',
            'config': 'default',
            'api': 'test',
            'authentication': {
                'type': 'client-credentials'
            }
        }
    )
)

queries = [
    Query(endpoint='search', parameters=[('q', 'test')])
]

options = RequestOptions(count=20, dev_version='master')

print(api.fetch(queries, options))
