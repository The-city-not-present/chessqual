"""FEN parsing and validation (stdlib only).

FEN (Forsyth–Edwards Notation) is the canonical text representation of a chess
position. This module validates the *structure* of a FEN string (field count,
ranks, piece letters, side to move, castling, en passant, and the move counters)
but does not perform full legality checking — that is out of scope for the core
and can be added later via an optional processor or a dedicated validator.
"""

from __future__ import annotations

# The six fields of a FEN record:
#   1. piece placement (ranks 8..1, files a..h)
#   2. side to move ("w" or "b")
#   3. castling availability
#   4. en passant target square
#   5. halfmove clock
#   6. fullmove number
_FIELD_COUNT = 6

_VALID_PIECES = frozenset("PNBRQKpnbrqk")
_SIDE_TO_MOVE = frozenset("wb")
_FILES = "abcdefgh"


def _validate_placement(placement: str) -> bool:
    ranks = placement.split("/")
    if len(ranks) != 8:
        return False
    for rank in ranks:
        if not rank:
            return False
        files = 0
        for ch in rank:
            if ch.isdigit():
                if ch == "0":
                    return False
                files += int(ch)
            elif ch in _VALID_PIECES:
                files += 1
            else:
                return False
        if files != 8:
            return False
    return True


def _validate_castling(castling: str) -> bool:
    if castling == "-":
        return True
    # Letters must be a non-empty, duplicate-free subset of KQkq.
    if set(castling) - set("KQkq"):
        return False
    return len(castling) == len(set(castling))


def _validate_en_passant(ep: str) -> bool:
    if ep == "-":
        return True
    if len(ep) != 2:
        return False
    return ep[0] in _FILES and ep[1] in "36"


def is_valid_fen(fen: str) -> bool:
    """Return True if ``fen`` is a structurally valid FEN record."""
    if not isinstance(fen, str):
        return False
    fields = fen.split()
    if len(fields) != _FIELD_COUNT:
        return False
    placement, side, castling, ep, halfmove, fullmove = fields
    if not _validate_placement(placement):
        return False
    if side not in _SIDE_TO_MOVE:
        return False
    if not _validate_castling(castling):
        return False
    if not _validate_en_passant(ep):
        return False
    try:
        if int(halfmove) < 0:
            return False
        if int(fullmove) < 1:
            return False
    except ValueError:
        return False
    return True
