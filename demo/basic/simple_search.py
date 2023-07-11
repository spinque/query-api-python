from query_api_python import Api, Query

api = Api(
    {
        'workspace': 'playground',
        'config': 'default',
        'api': 'test',
        'authentication': {
            'type': 'client-credentials'
        }
    }
)

queries = [
    Query(endpoint='/search', parameters=[('q', 'test')])
]

options = {'count': 20, 'devversion': 'master'}

print(api.fetch(queries, options))
