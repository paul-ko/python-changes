import functools


def output_multiplier(multiplier, func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        output = func(*args, **kwargs)
        return output * multiplier if output is not None else None

    return wrapper


multiplier_list = [
    functools.partial(output_multiplier, 0),
    functools.partial(output_multiplier, 1),
    functools.partial(output_multiplier, 2),
]


multiplier_map = {
    5: functools.partial(output_multiplier, 5),
    10: functools.partial(output_multiplier, 10),
}


@multiplier_list[2]
def add_then_times_2(a, b):
    return a + b


@multiplier_map[10]
def add_then_times_10(a, b):
    return a+b


def test_list_subscripting():
    assert add_then_times_2(2, 4) == 12


def test_map_subscripting():
    assert add_then_times_10(2, 4) == 60
