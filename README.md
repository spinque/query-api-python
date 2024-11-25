# spinque/query-api-python

Library to use the Spinque Query API in your Python project. 

The Spinque Query API is an HTTP API to retrieve search results for queries. Also check out the [documentation of the Spinque Query API](https://docs.spinque.com/3.0/using-apis/basic.html).

## Installing

Using [PyPi](https://pypi.org/project/spinque-query-api/):

```bash
$ pip install spinque-query-api
```

## Documentation

For documentation on the Spinque Query API itself, please see [this](https://docs.spinque.com/3.0/using-apis/basic.html).

### Defining queries

```python3

from spinque_query_api import Api, Query

api = Api(
    workspace='playground',
    config='default',
    api='test'
)


query = Query(endpoint='search', parameters=[('q', 'test')])
options = {'count': 20, 'dev_version': 'master'}

print(api.fetch(query, options))
```

### Authentication

Some Spinque APIs require authentication using OAuth 2.0. Support for the Client Credentials flow (for server applications) is provided through this library:

```python3
from spinque_query_api import Api, Query, Authentication

api = Api(
    workspace='demo08',
    config='default',
    api='demo',
    authentication=Authentication('auth_name')
)

queries = [
    Query(endpoint='test', parameters=[])
]

print(api.fetch(queries))
```

Note: the Client ID and Client Secret can be generated by creating a new System-to-System account in the Settings > Team Members section of Spinque Desk.
These can then be added in a `spinque.config` file that the Authentication module can work this. For more info about this, see the Spinque documentation. 
