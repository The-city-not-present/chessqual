# Project context

> Living document. Updated after every task. Read this first at the start of
> every task.

## What this is

`chessqual` is a small, personal tool for analyzing chess positions with
pluggable **processors**. A **position** is a single FEN; a **collection** is an
ordered list of positions (one position = a collection of length one). A
**processor** turns a position into an `Assessment` (score, mate, best move,
extras). The flagship processor is **Stockfish**; others are self-written (the
built-in `material` counter) or combinators. The core domain is stdlib-only.

## Layout

```
src/chessqual/
  positions/      # FEN validation, Position, Collection (stdlib-only)
  processors/     # Processor/Assessment contract, global registry, built-ins
    material/     #   self-written material-balance processor
    stockfish/    #   Stockfish processor (optional: python-chess + engine binary)
  analyze.py      # assess a collection with selected processors
tests/            # mirrors src/chessqual layout (pytest)
docs/
  roadmap.md
  project-context.md
.clinerules/      # machine rules (architecture, testing, domain model, ...)
```

## Decisions & reasoning

- **`src/` layout with a `chessqual` package** (rather than the sibling repos'
  flat `src/` modules) because this project has no pinliner bundling requirement
  and benefits from a single importable namespace (`import chessqual`) for tests,
  a future CLI, and a future UI.
- **FEN is the canonical position representation.** It is the universal,
  text-based chess interchange format and keeps the core dependency-free.
- **Core validates FEN structure, not legality.** Legality needs move generation
  and is out of scope for the core; it can be added via `python-chess` or a
  self-written validator later.
- **Processors are duck-typed (`name` + `assess`), not a class hierarchy**, so a
  self-written processor can be a plain object and combinators can wrap other
  processors freely.
- **`score` is side-to-move-relative centipawns** (positive = better for the side
  to move), matching engine output; color-relative processors convert to this
  convention before returning.
- **Optional dependencies follow the sibling projects' pattern**: global
  `requirements.txt` = app-wide only (just `pytest`); `python-chess` is declared
  per-processor in `stockfish/requirements.txt` and guarded with a `try/except`
  import so registration never breaks without it.
- **Built-in processors are registered explicitly** in
  `processors/__init__.py` (not auto-discovered) for the initial skeleton;
  auto-discovery is a roadmap item.

## Last state

- Added an **Apache-2.0 `LICENSE`** (verbatim, matching the sibling repos),
  updated the README license section, and marked the roadmap license item done.
- Added the GitHub remote `git@github.com:The-city-not-present/chessqual.git`
  and pushed the initial scaffold to `main`.
- Initial scaffold: `.clinerules/`, `docs/roadmap.md` + `docs/project-context.md`,
  `README.md`, `.gitignore`, `.env.example`, `requirements.txt`, `pytest.ini`,
  the `src/chessqual/` domain+processor skeleton, and a pytest suite mirroring
  the package layout (28 tests). Core is stdlib-only and importable; `material`
  works out of the box; `stockfish` is guarded and fails readably when
  `python-chess` or the engine binary is absent.

## Open questions

- Final project name (see `docs/roadmap.md`).
- First user surface: CLI vs web UI vs desktop.
- How much chess logic to keep self-written vs delegate to `python-chess`.

## Known gotchas

- Tests must be run from the repo root with `python -m pytest` (or `pytest`)
  so `pytest.ini`'s `pythonpath = src` is picked up.
- The `stockfish` processor is registered but only *usable* when `python-chess`
  is installed and an engine is reachable; its test only exercises the guarded
  failure path.
