# Chess domain model

The tool models chess positions and their assessment as a small, layered domain.
The authoritative source for the exact shapes is the code in `src/chessqual/`;
this file is a condensed summary.

## Position

- A **Position** is a single chess position, represented canonically by its
  **FEN** string (`src/chessqual/positions/position.py`).
- The core validates FEN **structure** only (6 fields, 8 ranks, valid piece
  letters, side to move, castling, en passant, halfmove/fullmove numbers) via
  `src/chessqual/positions/fen.py`. Full *legality* (legal move generation,
  checkmate/stalemate detection) is out of scope for the core and belongs to
  optional processors or a later validator.
- `Position.fen` is the canonical stored value; `Position.name` and
  `Position.meta` (an extensible dict) carry optional user metadata
  (comment, source game, tags, …) following the sibling projects' `meta` pattern.
- `Position.side_to_move` is derived from the FEN (`w` or `b`).

## Collection

- A **Collection** (`src/chessqual/positions/collection.py`) is an **ordered**
  list of Positions. Working with a single position is just a collection of
  length one — the tool always operates on a collection, so one-or-many is not a
  special case.

## Processor & Assessment

- A **Processor** is any object with a `name` and an
  `assess(position, **params) -> Assessment` method (duck-typed; see
  `src/chessqual/processors/base.py`). Processors are the **extensibility point**:
  Stockfish, self-written evaluators, and combinators that call other processors
  are all processors.
- An **Assessment** is the result of one processor on one position:
  `processor` (name), `score` (centipawns from the **side to move**'s perspective;
  positive = better for the side to move), `mate_in` (set instead when a forced
  mate is reported), `best_move`, `depth`, and an extensible `info` dict for
  processor-specific extras.
- The **score convention is side-to-move-relative** (matches engine output).
  A color-relative processor (e.g. material balance) converts to that convention
  before returning.

## Registry

- The **global registry** (`src/chessqual/processors/registry.py`) maps
  processor name → processor. There is one app-level instance, `registry`
  (lowercase), populated at import time in `src/chessqual/processors/__init__.py`.
- To add a processor: create a package under `src/chessqual/processors/` and
  register it in `src/chessqual/processors/__init__.py`. Auto-discovery is a
  possible later improvement (see `docs/roadmap.md`).
