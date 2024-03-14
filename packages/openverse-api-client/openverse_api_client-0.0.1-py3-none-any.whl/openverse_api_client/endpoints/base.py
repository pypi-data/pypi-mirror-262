from typing import Callable, Iterable
from abc import ABC


class OpenverseAPIEndpoint(ABC):
    method: str
    endpoint: str
    content_type: str = "application/json"
    path_params: Iterable[str] = ()
    params: type
    response: type
