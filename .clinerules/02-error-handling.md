# Error handling & validation

- **Fail early** with a **readable error message.** Detect wrong or missing
  things up front (e.g. an invalid FEN, a missing processor) rather than letting
  the program fail later with a cryptic error.
- **Do not over-validate.** Leave flexibility for real data formats; stay
  idiomatic to the language. The core validates FEN *structure*, not full chess
  legality — legality is a separate concern.
- **Respect mathematical and logical validity.** Don't reject valid cases just
  because they're unusual, empty, or degenerate (e.g. a collection of a single
  position is the normal case, not a special case).
