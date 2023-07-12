from query_api_python import Api, Query

api = Api(
    {
        'workspace': 'demo08',
        'config': 'default',
        'api': 'demo',
        'authentication': {
            'authServer': 'https://login.spinque.com',
            'clientId': '0T1eIL2Ha29ZTCh9YXjU4yIRxFd8FUXC',
            'clientSecret': '-p7_liXfXFg1fKnsuTv4_0CvbegNn3Fvp640IYslIJNnyZtX2qSUVZ0qb6YtxMIB'
        }
    }
)

queries = [
    Query(endpoint='test', parameters=[])
]

print(api.fetch(queries))
