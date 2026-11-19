import pytest
from combine_dicts import combine_dicts
@pytest.mark.parametrize("d1, d2, expected", [
    ({"a": 1, "b": 2}, {"c": 3, "d": 4}, {"a": 1, "b": 2, "c": 3, "d": 4}),
    ({"a": 1, "b": 2}, {"b": 20, "c": 3}, {"a": 1, "b": 20, "c": 3}),
    ({}, {"a": 1}, {"a": 1}),
    ({"a": 1}, {}, {"a": 1}),
    ({}, {}, {}),
])
def test_combine_dicts(d1, d2, expected):
    d1_before = d1.copy()
    d2_before = d2.copy()
    result = combine_dicts(d1, d2)
    assert result == expected
    assert list(result.keys()) == list(expected.keys())
    assert d1 == d1_before
    assert d2 == d2_before