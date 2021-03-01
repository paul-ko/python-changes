import pytest


#################
# basic success #
#################


def test_simple_union():
    a = {"a": 1}
    b = {"b": 2}
    a |= b

    assert len(a) == 2
    assert a["a"] == 1
    assert a["b"] == 2

    assert len(b) == 1
    assert b["b"] == 2


# noinspection PyTypeChecker
def test_different_key_types():
    a = {"a": 1}
    b = {0: 2}
    a |= b

    assert len(a) == 2
    assert a["a"] == 1
    assert a[0] == 2

    assert len(b) == 1
    assert b[0] == 2


def test_last_seen_wins():
    a = {"a": "first"}
    b = {"a": "second"}
    a |= b

    assert len(a) == 1
    assert a["a"] == "second"

    assert len(b) == 1
    assert b["a"] == "second"


def test_union_with_empty():
    a = {"a": 1}
    b = {}
    a |= b

    assert len(a) == 1
    assert a["a"] == 1

    assert not len(b)


#####################
# key-value support #
#####################
# Only for augmented.


def test_simple_key_value_union():
    a = {"a": 1}
    b_kv = [("b", 2)]
    a |= b_kv

    assert len(a) == 2
    assert a["a"] == 1
    assert a["b"] == 2


# noinspection PyTypeChecker
def test_key_value_union_different_key_types():
    a = {"a": 1}
    b_kv = [(0, 2)]
    a |= b_kv

    assert len(a) == 2
    assert a["a"] == 1
    assert a[0] == 2


def test_key_value_union_last_seen_wins():
    a = {"a": "first"}
    b_kv = [("a", "second")]
    a |= b_kv

    assert len(a) == 1
    assert a["a"] == "second"


def test_key_value_union_with_empty():
    a = {"a": "first"}
    b_kv = []
    a |= b_kv

    assert len(a) == 1
    assert a["a"] == "first"


####################
# Mapping protocol #
####################


class MinimalMap:
    def __init__(self, d):
        self._d = d

    def keys(self):
        return self._d.keys()

    def __getitem__(self, item):
        return self._d.__getitem__(item)


def test_mapping_protocol_union():
    a = {"a": 1}
    z = {"b": 2}
    b = MinimalMap(z)
    a |= b

    assert len(a) == 2
    assert a["a"] == 1
    assert a["b"] == 2


##########
# errors #
##########


def test_union_with_none():
    a = {"a": 1}
    with pytest.raises(TypeError):
        a |= None


def test_union_with_list_containing_empty_tuple():
    a = {"a": 1}
    with pytest.raises(ValueError):
        a |= [()]
