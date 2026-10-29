import pytest

pytest.importorskip("flask")

from chessqual.web.adapters.flask_app import create_flask_app

START_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"


def test_flask_app_serves_page_and_api():
    app = create_flask_app()
    client = app.test_client()

    resp = client.get("/")
    assert resp.status_code == 200
    assert b"hello" in resp.data.lower()

    health = client.get("/api/health")
    assert health.status_code == 200
    assert health.get_json()["status"] == "ok"

    processors = client.get("/api/processors")
    assert "material" in processors.get_json()["processors"]

    assess = client.post(
        "/api/assess", json={"fens": [START_FEN], "processors": ["material"]}
    )
    assert assess.status_code == 200
    assert assess.get_json()["results"][0]["assessments"]["material"]["score"] == 0
