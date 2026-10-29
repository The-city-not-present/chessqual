# TODOs

This section captures everything that comes to mind that should ideally be
updated or decided. Tasks listed here are not necessarily the highest priority.

- **Decide the project name.** The directory/package is `chessqual` for now; it
  is provisional. Decide a final display name and whether the package should be
  renamed before it gains users.
- **Decide UI or no UI.** The core is library-only today (import `chessqual` and
  call `analyze`). Decide the first user surface: a small CLI, then optionally a
  local web UI (the sibling projects use a Python backend + plain-JS frontend, no
  Flask/Django), or a desktop wrapper. (Started: added an optional
  `chessqual.web` backend layer — framework-free handlers + a `ROUTES` table +
  Flask/webserve adapters + a minimal HTML page; the real frontend is still TBD.)
- **Decide how much chess logic is self-written.** The core validates FEN
  structure only. Decide whether to pull in `python-chess` app-wide for legal
  moves/legality, or keep it optional per-processor and write our own move
  generation/legality where it is educational to do so.
- **Finish the Stockfish processor.** It currently shells out via `python-chess`
  (`SimpleEngine`) and returns one `Assessment`. Consider: multi-PV, per-move
  analysis, engine options (hash/threads), and UCI session reuse.
- **Add more processors.** Candidates: a self-written material+positional
  evaluator, a legal-move counter, an endgame-tablebase probe, and *combinator*
  processors that aggregate other processors' results (e.g. average, vote,
  report table).
- **Persistence.** Decide how collections are stored/loaded: FEN text files,
  JSON/YAML, or SQLite (the sibling projects already use YAML and SQLite
  storage layers that could be reused).
- **Assessment result storage.** Decide whether assessments are kept in memory
  only, or persisted with timestamps (see `.clinerules/06-dates-and-time.md`).
- **Auto-discovery of processors.** Today built-in processors are registered
  explicitly in `src/chessqual/processors/__init__.py`. Consider automatic
  discovery of processor packages (with the same optional-dependency guard).
- **License.** The sibling projects are Apache-2.0; decide and add a `LICENSE`
  file. (Done: added an Apache-2.0 `LICENSE` file.)
