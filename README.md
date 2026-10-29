# ChessQual

A small, personal tool for **analyzing chess positions** with pluggable
processors — starting with Stockfish, but built to grow into self-written
evaluators and combinators. Educational, hobby, research; always with an eye on
growing into something bigger.

## What it does

- **Load positions.** A single FEN, or a whole collection of them. Working with
  one position is just a collection of length one, so the tool always operates
  on a collection.
- **Assess positions with processors.** Processors are defined at the global app
  level and are the extensibility point. Each processor turns a position into an
  `Assessment`.
- **Stockfish** is the flagship processor (optional dependency; needs the engine
  binary and `python-chess`).
- **Self-written processors** — e.g. the built-in material-count processor — and
  later **combinators** that aggregate other processors' results.

## Core concepts

| Concept | What it is | Where |
| --- | --- | --- |
| `Position` | one position, stored canonically as FEN | `src/chessqual/positions/` |
| `Collection` | an ordered list of positions (one-or-many) | `src/chessqual/positions/` |
| `Processor` | duck-typed `assess(position) -> Assessment` | `src/chessqual/processors/` |
| `Assessment` | one processor's result (score, mate, best move, info) | `src/chessqual/processors/` |
| `registry` | the global name → processor registry | `src/chessqual/processors/` |

The core domain is **stdlib-only**; everything else is an optional per-processor
dependency.

## Quick start

You need Python 3.10+.

```bash
python3 -m venv .venv
source .venv/bin/activate            # Windows: .venv\Scripts\activate
pip install -r requirements.txt      # app-wide: pytest (core needs no deps)

# optional, for the Stockfish processor:
pip install -r src/chessqual/processors/stockfish/requirements.txt
# and point the tool at your engine (or put `stockfish` on PATH):
export STOCKFISH_PATH=/path/to/stockfish

python -m pytest                     # run the test suite
```

## Usage (from a Python shell)

```python
from chessqual import Collection, registry
from chessqual.analyze import assess

collection = Collection.from_fens([
    "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
])

print(registry.names())              # e.g. ['material', 'stockfish']
print(assess(collection, ["material"]))
```

## Web UI (optional, backend + minimal page)

The optional web layer (`src/chessqual/web/`) serves a JSON API and a minimal
HTML page on `localhost`. It is written framework-free: the same endpoints can
be served by **Flask** or by your self-written **webserve** server.

```bash
pip install -r src/chessqual/web/requirements.txt   # Flask (optional)

# Flask (default):
PYTHONPATH=src python -m chessqual.web --server flask --port 5000

# webserve (self-written, included as a git submodule):
PYTHONPATH=src python -m chessqual.web --server webserve
```

Then open the printed address (e.g. http://localhost:5000/).

Endpoints:

- `GET /` — minimal landing page
- `GET /api/health` — `{"status": "ok", "version": ...}`
- `GET /api/processors` — `{"processors": [...]}`
- `POST /api/assess` — body `{"fens": [...], "processors": [...]}` → per-position assessments

## Documentation

- **Roadmap / TODOs** — [`docs/roadmap.md`](docs/roadmap.md).
- **Project state log** — [`docs/project-context.md`](docs/project-context.md).
- **Machine rules** — the `.clinerules/` directory.

## License

[Apache License 2.0](LICENSE).
