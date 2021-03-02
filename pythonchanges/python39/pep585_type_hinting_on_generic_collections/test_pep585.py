"""
Applies to a large number of types, including many that weren't supported by `typing`.
"""
import types

from _pytest.python import Metafunc
import pytest


def test_issubclass_second_arg_one_parametrized_type(
    parametrized_type, type_parameters
):
    with pytest.raises(TypeError):
        # noinspection PyTypeHints
        issubclass(parametrized_type, parametrized_type[type_parameters])


def test_isinstance_second_arg_parametrized_type(parametrized_type, type_parameters):
    with pytest.raises(TypeError):
        # noinspection PyTypeHints
        issubclass(parametrized_type, parametrized_type[type_parameters])


def test_isinstance_of_genericalias(parametrized_type, type_parameters):
    assert isinstance(parametrized_type[type_parameters], types.GenericAlias)


def test_isinstance_of_nongeneric(parametrized_type, type_parameters):
    assert isinstance(parametrized_type[type_parameters](), parametrized_type)


def test_type(parametrized_type, type_parameters):
    a: parametrized_type[type_parameters] = parametrized_type()
    b: parametrized_type = parametrized_type()
    assert type(a) == type(b)


def pytest_generate_tests(metafunc: Metafunc):
    parametrized_type_fixture = "parametrized_type"
    type_parameters_fixture = "type_parameters"
    parametrized_types = [
        (list, [str]),
        (set, [str]),
        (frozenset, [str]),
        (tuple, [str]),
        (dict, [str, str]),
    ]

    if parametrized_type_fixture in metafunc.fixturenames:
        metafunc.parametrize(
            parametrized_type_fixture,
            [o[0] for o in parametrized_types],
            ids=[str(s[0]) for s in parametrized_types],
        )
        metafunc.parametrize(
            type_parameters_fixture,
            [o[1] for o in parametrized_types],
        )
