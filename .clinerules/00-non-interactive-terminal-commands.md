# Non-interactive terminal commands

- Always use `git --no-pager` for Git commands (e.g. `git log --no-pager`) so a
  pager never blocks the terminal waiting for input.
- Avoid interactive commands and pagers in terminal sessions; prefer
  non-interactive alternatives that exit automatically.
- Fallback: if a pager can still start (e.g. a Git command run without
  `--no-pager`), disable it by setting pager environment variables first:
  `GIT_PAGER=cat PAGER=cat`. This makes any pager print and exit immediately
  instead of waiting for a key press.
- Last resort: if a command does get stuck in an interactive pager, do not type
  `q` and rely on the partial output — re-run the command with `--no-pager` (or
  the environment variables above) so the full output is captured.
