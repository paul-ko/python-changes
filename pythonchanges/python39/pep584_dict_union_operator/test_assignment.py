import pytest


#################
# basic success #
#################


def test_simple_union():
    a = {"a": 1}
    b = {"b": 2}
    ab = a | b

    assert len(ab) == 2
    assert ab["a"] == 1
    assert ab["b"] == 2

    assert len(a) == 1
    assert a["a"] == 1

    assert len(b) == 1
    assert b["b"] == 2


# noinspection PyTypeChecker
def test_different_key_types():
    a = {"a": 1}
    b = {0: 2}
    ab = a | b

    assert len(ab) == 2
    assert ab["a"] == 1
    assert ab[0] == 2

    assert len(a) == 1
    assert a["a"] == 1

    assert len(b) == 1
    assert b[0] == 2


def test_last_seen_wins():
    a = {"a": "first"}
    b = {"a": "second"}
    ab = a | b

    assert len(ab) == 1
    assert ab["a"] == "second"

    assert len(a) == 1
    assert a["a"] == "first"

    assert len(b) == 1
    assert b["a"] == "second"


def test_union_with_empty():
    a = {"a": 1}
    b = {}
    ab = a | b

    assert len(ab) == 1
    assert ab["a"] == 1

    assert len(a) == 1
    assert a["a"] == 1

    assert not len(b)


def test_triple_union():
    a = {"a": 1}
    b = {"b": 2}
    bc = {"b": 3, "c": 3}
    abc = a | b | bc

    assert len(abc) == 3
    assert abc["a"] == 1
    assert abc["b"] == 3
    assert abc["c"] == 3

    assert len(a) == 1
    assert a["a"] == 1

    assert len(b) == 1
    assert b["b"] == 2

    assert len(bc) == 2
    assert bc["b"] == 3
    assert bc["c"] == 3


##########
# errors #
##########


# noinspection PyTypeChecker
def test_union_with_none():
    a = {"a": 1}
    with pytest.raises(TypeError):
        _ = a | None


# noinspection PyTypeChecker
def test_union_with_key_value():
    a = {"a": 1}
    b = [("b", 2)]
    with pytest.raises(TypeError):
        _ = a | b
