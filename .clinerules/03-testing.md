# Testing

Write automated tests for **every isolated module** — anything with clear inputs
and an expected outcome: FEN validation, the Position/Collection model, the
processor registry, and each processor's assessment logic.

Do **not** write tests for pure bootstrapping/smoke ("the module imports", "the
app starts"). That is hard to test meaningfully and its breakage is obvious by
inspection. Test the *logic*, not the shell.

## Principles

- **The module is the test unit.** Modules are encapsulated with explicit inputs
  and outputs, so each behaviour gets a test: the normal case, edge/empty cases,
  and expected failures.
- **Deterministic and independent.** One behaviour per test where practical; no
  test-order dependence; no reliance on real network, filesystem, or wall clock
  unless that is the exact thing under test (then keep it small and explicit).
  Processors that need an external engine (Stockfish) are tested for their
  *guarded failure path* so the suite passes without the engine installed.
- **Isolation enables testing.** If a piece of logic is hard to test, extract it
  into a module with clearer boundaries (see `01-architecture-imports.md`).

## Layout

**Python → `pytest`.** Tests live in a top-level `tests/` directory that mirrors
the `src/chessqual/` package layout:

```
src/chessqual/
  positions/
    fen.py
  processors/
    material/
      processor.py
tests/
  positions/
    test_fen.py
  processors/
    test_material.py
```

Name files `test_*.py` and test functions `test_*`. Tests import the code under
test through its public package path (`from chessqual.positions.fen import ...`).
Run the suite from the repo root with `python -m pytest` (see `pytest.ini`).
