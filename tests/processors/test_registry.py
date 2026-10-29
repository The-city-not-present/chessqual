import pytest

from chessqual.processors import registry
from chessqual.processors.base import Assessment
from chessqual.processors.registry import Registry


class _Dummy:
    name = "dummy"

    def assess(self, position, **params):
        return Assessment(processor=self.name)


def test_global_registry_has_builtin_processors():
    assert "material" in registry
    assert "stockfish" in registry
    assert set(registry.names()) >= {"material", "stockfish"}


def test_register_and_get():
    r = Registry()
    r.register(_Dummy())
    assert r.get("dummy").name == "dummy"


def test_duplicate_registration_fails():
    r = Registry()
    r.register(_Dummy())
    with pytest.raises(ValueError):
        r.register(_Dummy())


def test_unknown_processor_raises_readable_error():
    r = Registry()
    with pytest.raises(KeyError, match="unknown processor"):
        r.get("nope")


def test_len_and_contains():
    r = Registry()
    assert len(r) == 0
    r.register(_Dummy())
    assert len(r) == 1
    assert "dummy" in r
    assert "nope" not in r
