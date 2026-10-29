import pytest

webserve_ws = pytest.importorskip("webserver_engine.webserve.src.webserver")

from chessqual.web.adapters.webserve_endpoints import build_webserve_endpoints


class _FakeRequestHandler:
    def __init__(self, command="GET", path="/", body=b""):
        self.command = command
        self.path = path
        self._body = body

    @property
    def request_body(self):
        class _Reader:
            def __init__(self, data):
                self.data = data

            def read(self):
                return self.data

        return _Reader(self._body)


def test_response_converts_to_webserve_webresponse():
    endpoints = build_webserve_endpoints()
    resp = endpoints["/api/processors"](_FakeRequestHandler("GET", "/api/processors"))
    converted = webserve_ws.WebResponse.from_existing(resp)
    assert converted.status_code == 200
    assert converted.content_type == "application/json"
    assert "material" in converted.body
