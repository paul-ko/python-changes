import collections
from dataclasses import dataclass
from typing import Generic
from typing import TypeVar

import pytest


class CustomString(collections.UserString):
    def __repr__(self):
        return f'CustomString("{self}")'


class CustomCustomString(CustomString):
    def __repr__(self):
        return f'CustomCustomString("{self}")'


T = TypeVar("T", str, CustomString, bytes, bytearray)


@dataclass(frozen=True)
class Case(Generic[T]):
    base: T
    affix: T
    nonexistent_affix: T
    empty_affix: T
    prefix_removed: T
    suffix_removed: T


test_strings = [
    Case("abcab", "ab", "zz", "", "cab", "abc"),
    Case(
        CustomString("abcab"),
        CustomString("ab"),
        CustomString("zz"),
        CustomString(""),
        CustomString("cab"),
        CustomString("abc"),
    ),
    Case(b"abcab", b"ab", b"zz", b"", b"cab", b"abc"),
    Case(
        bytearray(b"abcab"),
        bytearray(b"ab"),
        bytearray(b"zz"),
        bytearray(b""),
        bytearray(b"cab"),
        bytearray(b"abc"),
    ),
]

test_ids = [repr(s.base) for s in test_strings]
paramatrizer = pytest.mark.parametrize("case", test_strings, ids=test_ids)


#################
# remove_prefix #
#################


@paramatrizer
def test_remove_existing_prefix(case: Case):
    assert case.base.removeprefix(case.affix) == case.prefix_removed


@paramatrizer
def test_remove_nonexistent_prefix(case: Case):
    assert case.base.removeprefix(case.nonexistent_affix) == case.base


@paramatrizer
def test_remove_empty_prefix(case: Case):
    assert case.base.removeprefix(case.empty_affix) == case.base


def test_remove_subclass_prefix():
    base = CustomString("abc")
    to_remove = CustomCustomString("ab")
    processed = base.removeprefix(to_remove)
    assert processed == CustomString("c")
    assert type(processed) is CustomString


def test_remove_superclass_prefix():
    base = CustomCustomString("abc")
    to_remove = CustomString("ab")
    processed = base.removeprefix(to_remove)
    assert processed == CustomCustomString("c")
    assert type(processed) is CustomCustomString


def test_remove_incompatible_type_prefix():
    with pytest.raises(TypeError):
        # noinspection PyTypeChecker
        b"ab".removeprefix("a")


#################
# remove_suffix #
#################


@paramatrizer
def test_remove_existing_suffix(case: Case):
    assert case.base.removesuffix(case.affix) == case.suffix_removed


@paramatrizer
def test_remove_nonexistent_suffix(case: Case):
    assert case.base.removesuffix(case.nonexistent_affix) == case.base


@paramatrizer
def test_remove_empty_suffix(case: Case):
    assert case.base.removesuffix(case.empty_affix) == case.base


def test_remove_subclass_suffix():
    base = CustomString("abc")
    to_remove = CustomCustomString("bc")
    processed = base.removesuffix(to_remove)
    assert processed == CustomString("a")
    assert type(processed) is CustomString


def test_remove_superclass_suffix():
    base = CustomCustomString("abc")
    to_remove = CustomString("bc")
    processed = base.removesuffix(to_remove)
    assert processed == CustomCustomString("a")
    assert type(processed) is CustomCustomString


def test_remove_incompatible_type_suffix():
    with pytest.raises(TypeError):
        # noinspection PyTypeChecker
        b"ab".removesuffix("a")
