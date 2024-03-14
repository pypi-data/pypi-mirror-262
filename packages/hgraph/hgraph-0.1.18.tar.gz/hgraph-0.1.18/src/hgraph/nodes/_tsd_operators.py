from dataclasses import field, dataclass
from typing import Type, Mapping

from hgraph import TS, SCALAR, TIME_SERIES_TYPE, TSD, compute_node, REMOVE_IF_EXISTS, REF, \
    STATE, graph, contains_, not_, K, NUMBER, CompoundScalar
from hgraph._types._time_series_types import K_1
from hgraph.nodes import sum_
from hgraph.nodes._operators import len_
from hgraph.nodes._set_operators import is_empty

__all__ = ("make_tsd", "flatten_tsd", "extract_tsd", "tsd_get_item", "tsd_contains", "tsd_not", "tsd_is_empty")


@compute_node(valid=("key",))
def make_tsd(key: TS[K_1], value: TS[SCALAR], remove_key: TS[bool] = None,
             ts_type: Type[TIME_SERIES_TYPE] = TS[SCALAR]) -> TSD[K_1, TIME_SERIES_TYPE]:
    """
    Make a TSD from a time-series of key and value, if either key or value ticks an entry in the TSD will be
    created / update. It is also possible to remove a key by setting remove_key to True.
    In this scenario a key will be removed if the remove_key ticked True or if the key ticks and remove_key is already
    set to True.
    """

    if remove_key.valid:
        if remove_key.value and remove_key.modified or key.modified:
            return {key.value: REMOVE_IF_EXISTS}
        elif key.modified or value.modified:
            return {key.value: value.delta_value}
    else:
        return {key.value: value.delta_value}


@compute_node
def flatten_tsd(tsd: TSD[K_1, TIME_SERIES_TYPE]) -> TS[Mapping[K_1, SCALAR]]:
    """
    Flatten a TSD into a time-series of frozen dicts (equivalent to the delta dictionary)
    """
    return tsd.delta_value


@compute_node
def extract_tsd(ts: TS[Mapping[K_1, SCALAR]]) -> TSD[K_1, TIME_SERIES_TYPE]:
    """
    Extracts a TSD from a stream of delta dictionaries.
    """
    return ts.value


@dataclass
class KeyValueRefState:
    reference: object = field(default_factory=object)
    tsd: TSD[SCALAR, TIME_SERIES_TYPE] | None = None
    key: SCALAR | None = None


@compute_node
def tsd_get_item(tsd: REF[TSD[K, TIME_SERIES_TYPE]], key: TS[K], _ref: REF[TIME_SERIES_TYPE] = None,
                 _state: STATE[KeyValueRefState] = None) -> REF[TIME_SERIES_TYPE]:
    """
    Returns the time-series associated to the key provided.
    """
    # Use tsd as a reference to avoid the cost of the input wrapper
    # If we got here something was modified so release any previous value and replace
    if tsd.modified or key.modified:
        if _state.tsd is not None:
            _ref.make_passive()
            _state.tsd.release_ref(_state.key, _state.reference)
        if tsd.value.valid:
            _state.tsd = tsd.value.output
            _state.key = key.value
        else:
            _state.tsd = None
            _state.key = None
        output = _state.tsd.get_ref(_state.key, _state.reference)
        _ref.bind_output(output)
        _ref.make_active()
    return _ref.value


@graph(overloads=contains_)
def tsd_contains(ts: TSD[K, TIME_SERIES_TYPE], item: TS[K]) -> TS[bool]:
    """Contains for TSD delegates to the key-set contains"""
    return contains_(ts.key_set, item)


@graph(overloads=not_)
def tsd_not(ts: TSD[K, TIME_SERIES_TYPE]) -> TS[bool]:
    return not_(ts.key_set)


@graph(overloads=is_empty)
def tsd_is_empty(ts: TSD[K, TIME_SERIES_TYPE]) -> TS[bool]:
    return is_empty(ts.key_set)


@graph(overloads=len_)
def tsd_len(ts: TSD[K, TIME_SERIES_TYPE]) -> TS[int]:
    return len_(ts.key_set)


@compute_node(overloads=sum_)
def sum_tsd(ts: TSD[K, TS[NUMBER]]) -> TS[NUMBER]:
    return sum(i.value for i in ts.valid_values())
