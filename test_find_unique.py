import pytest
from find_unique import find_unique
@pytest.mark.parametrize("items, expected", [
    ([1, 2, 2, 3, 4, 3, 5], [1, 4, 5]),
    (["a", "b", "a", "c"], ["b", "c"]),
    ([1, 2, 3], [1, 2, 3]),
    ([7, 7, 7], []),
    ([], []),
    ([10], [10]),
])
def test_find_unique(items, expected):
    assert find_unique(items) == expected