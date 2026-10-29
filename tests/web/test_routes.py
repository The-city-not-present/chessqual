from chessqual.web.routes import ROUTES


def test_expected_paths_and_methods():
    table = {route.path: route.methods for route in ROUTES}
    assert table["/"] == frozenset({"GET"})
    assert table["/api/health"] == frozenset({"GET"})
    assert table["/api/processors"] == frozenset({"GET"})
    assert table["/api/assess"] == frozenset({"POST"})
