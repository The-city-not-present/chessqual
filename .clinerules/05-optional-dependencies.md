# Optional dependencies

- The global `requirements.txt` lists only app-wide requirements. The core
  domain (`chessqual.positions`) is stdlib-only.
- Per-processor extras are *optional*: keep a `requirements.txt` next to the
  processor (encapsulation), e.g.
  `src/chessqual/processors/stockfish/requirements.txt`.
- Optional deps may be platform-specific or heavy; a missing one is normal and
  must not break processor discovery/registration.
- Each processor that needs extra packages guards its own import (`try/except`,
  storing the error) so the module always loads and the processor is always
  registered; its `assess` raises a readable error (chained to the original) at
  its start. No global import-error machinery.
- A processor that needs an external binary (Stockfish) resolves it lazily at
  assessment time (explicit path → `STOCKFISH_PATH` env var → `PATH` lookup) and
  raises a readable error if it is absent.
