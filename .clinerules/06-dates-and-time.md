# Dates & time

- **Store in UTC.** Timestamps produced or stored by the program are in UTC.
  Full timestamps are ISO-8601 with an explicit UTC designator
  (`2025-07-15T10:00:00Z`); calendar dates with no time are `YYYY-MM-DD`.
- **No hardcoded dates.** Don't put dates in implementation code. Dates come
  from data, or are generated when an object is created (e.g.
  `datetime.now(timezone.utc)`).
- Applies to any future metadata (e.g. when a position/collection was added or
  an assessment was produced). There is no UI timezone handling yet.
