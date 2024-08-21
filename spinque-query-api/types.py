import json

from enum import Enum
from typing import List, Tuple


class Query:

    def __init__(self, endpoint: str, parameters: List[Tuple[str, str]] = None):
        self.endpoint = endpoint
        self.parameters = parameters


class RequestType(Enum):
    RESULTS = 1
    STATISTICS = 2

    def __str__(self) -> str:
        return 'results' if self.name == 'RESULTS' else 'statistics'


class RequestOptionsFormat(Enum):
    JSON = 1
    XML = 2
    RDF = 3
    CSV = 4
    XLSX = 5
