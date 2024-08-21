from spinque_query_api import Api, Query

api = Api(
    {
        'workspace': 'demo08',
        'config': 'default',
        'api': 'demo',
        'authentication': {
            'authServer': 'https://login.spinque.com'
        }
    }
)

queries = [
    Query(endpoint='test', parameters=[])
]

print(api.fetch(queries))
