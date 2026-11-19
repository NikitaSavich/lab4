import pytest
from are_anagrams import are_anagrams
@pytest.mark.parametrize("a, b, expected", [
    ("listen", "silent", True),
    ("Listen", "Silent", True),
    ("клоун", "колун", True),
    ("hello", "world", False),
    ("abc", "abcd", False),
    ("test", "test", False),
    ("Test", "test", False),
    ("", "", False),
])
def test_are_anagrams(a, b, expected):
    assert are_anagrams(a, b) == expected