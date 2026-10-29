"""Run the chessqual web server: ``python -m chessqual.web``."""

from __future__ import annotations

import argparse


def main(argv=None) -> None:
    parser = argparse.ArgumentParser(
        prog="chessqual.web",
        description="Serve the chessqual web UI on localhost.",
    )
    parser.add_argument("--server", choices=("flask", "webserve"), default="flask")
    parser.add_argument("--host", default="localhost")
    parser.add_argument("--port", type=int, default=None)
    args = parser.parse_args(argv)

    if args.server == "flask":
        _run_flask(args.host, args.port)
    else:
        _run_webserve(args.host, args.port)


def _run_flask(host: str, port: int | None) -> None:
    from .adapters.flask_app import create_flask_app

    port = port or 5000
    app = create_flask_app()
    print(f"chessqual web (flask) → http://{host}:{port}")
    app.run(host=host, port=port, debug=False)


def _run_webserve(host: str, port: int | None) -> None:
    from .adapters.webserve_endpoints import build_webserve_endpoints

    try:
        from webserver_engine.webserve.src.webserver import Webserver
        from webserver_engine.webserve.src.find_free_port import find_free_port
        from webserver_engine.webserve.src.launch_browser import launch_browser
    except ImportError as exc:
        raise SystemExit(
            "webserve is not importable; add it as a submodule at "
            "src/webserver_engine/webserve (git submodule add "
            "https://github.com/The-city-not-present/webserve.git "
            "src/webserver_engine/webserve) and run with PYTHONPATH=src."
        ) from exc

    port = port or find_free_port(host, start=5180)
    config = {
        "http_host": host,
        "http_port": port,
        "http_protocol": "http",
        "http_address": f"http://{host}:{port}",
    }
    server = Webserver(config, is_threading=True)
    server.assign_handlers(build_webserve_endpoints())
    print(f"chessqual web (webserve) → http://{host}:{port}")
    launch_browser(f"http://{host}:{port}/")
    server.run()


if __name__ == "__main__":
    main()
