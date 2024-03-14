import pytest
from frozendict import frozendict

from hgraph import TS, graph, TIME_SERIES_TYPE, SCALAR_2, TSD, REMOVE, not_, SCALAR
from hgraph.nodes import make_tsd, extract_tsd, flatten_tsd, is_empty, sum_
from hgraph.test import eval_node


def test_make_tsd():
    assert eval_node(make_tsd, ['a', 'b', 'a'], [1, 2, 3]) == [{'a': 1}, {'b': 2}, {'a': 3}]


def d(d):
    return frozendict(d)


def test_flatten_expand_tsd():
    @graph
    def flatten_expand_test(ts: TS[frozendict[str, int]]) -> TS[frozendict[str, int]]:
        tsd = extract_tsd[TIME_SERIES_TYPE: TS[int]](ts)
        return flatten_tsd[SCALAR: int](tsd)

    assert eval_node(flatten_expand_test, [{'a': 1}, {'b': 2}, {'a': 3}]) == [{'a': 1}, {'b': 2}, {'a': 3}]


def test_is_empty():
    @graph
    def is_empty_test(tsd: TSD[int, TS[int]]) -> TS[bool]:
        return is_empty(tsd)

    assert eval_node(is_empty_test, [None, {1: 1}, {2: 2}, {1: REMOVE}, {2: REMOVE}]) == [True, False, None, None, True]


def test_not():
    @graph
    def is_empty_test(tsd: TSD[int, TS[int]]) -> TS[bool]:
        return not_(tsd)

    assert eval_node(is_empty_test, [None, {1: 1}, {2: 2}, {1: REMOVE}, {2: REMOVE}]) == [True, False, None, None, True]


@pytest.mark.parametrize(
    ["inputs", "expected"],
    [
        [[{0: 1, 1: 2}, {0: 2, 1: 3}], [3, 5]],
        [[{0: 1.0, 1: 2.0}, {0: 2.0, 1: 3.0}], [3.0, 5.0]],
    ]
)
def test_sum(inputs, expected):
    assert eval_node(sum_, inputs, resolution_dict={'ts': TSD[int, TS[type(inputs[0][0])]]}) == expected
