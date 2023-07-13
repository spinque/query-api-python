# spinque/query-api-python

Library to use the Spinque Query API in your Python project. 

The Spinque Query API is an HTTP API to retrieve search results for queries. Also check out the [documentation of the Spinque Query API](https://docs.spinque.com/3.0/using-apis/basic.html).

## Installing

Not released yet on PyPI, but it will be: 

Using PyPi:

```bash
$ pip install spinque-api
```

## Documentation

For documentation on the Spinque Query API itself, please see [this](https://docs.spinque.com/3.0/using-apis/basic.html).

### Defining queries

```python3

from query_api_python import Api, Query

api = Api(
    {
        'workspace': 'playground',
        'config': 'default',
        'api': 'test'
    }
)


query = Query(endpoint='search', parameters=[('q', 'test')])
options = {'count': 20, 'dev_version': 'master'}

print(api.fetch(query, options))
```

### Authentication

Some Spinque APIs require authentication using OAuth 2.0. Support for the Client Credentials flow (for server applications) is provided through this library:

```python3
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
```

Note: the Client ID and Client Secret can be generated by creating a new System-to-System account in the Settings > Team Members section of Spinque Desk.
