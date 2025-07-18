from __future__ import annotations

from jsonbourne import JsonObj
from jsonbourne.httpx import Client


def test_response_dot_JSON() -> None:
    something_url = "https://jsonplaceholder.typicode.com/todos/1"
    c = Client()
    r = c.get(something_url)
    json_dict = r.json()
    assert isinstance(json_dict, dict)
    assert hasattr(r, "JSON")
    assert callable(r.JSON)
    jsonobj = r.JSON()
    assert isinstance(jsonobj, JsonObj), "r.JSON() should return a JsonObj object"
    assert jsonobj == json_dict, "r.JSON() should return the same as r.json()"
