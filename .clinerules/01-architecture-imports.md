# Architecture & imports

- **Relative imports only.** Import neighbours via `from .` / `from ..` inside the
  `chessqual` package. Never import through an app-root or absolute path, so each
  module stays self-contained and can be relocated without breaking callers.
- **Independent, reusable modules.** A module can be moved or extracted into its
  own package (or, later, a submodule). Keep its public surface explicit and its
  dependencies close; minimize reaching outside its folder.
- **Every package has `__init__.py`.** When adding a package or subpackage, ensure
  each level has an `__init__.py` (consistent with the sibling repos, even though
  modern Python does not strictly require it).
- **The package is `src/chessqual/`** (the "src layout"). Import it as `chessqual`
  (tests set `pythonpath = src` in `pytest.ini`). Application code and a future
  CLI/UI live here; keep the core domain (`positions`) dependency-free.
