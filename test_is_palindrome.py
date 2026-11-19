import pytest
from is_palindrome import is_palindrome
@pytest.mark.parametrize("value, expected", [
    ("level", True),
    ("Madam", True),
    ("Топот", True),
    ("python", False),
    (12321, True),
    (12345, False),
    (-121, False),
    (0, True),
    ("a", True),
    ("", True),
])
def test_is_palindrome(value, expected):
    assert is_palindrome(value) == expected