import pytest
from count_words import count_words
@pytest.mark.parametrize("text, expected", [
    ("Hello world", 2),
    ("Один два три четыре", 4),
    ("   много    пробелов   между   словами  ", 4),
    ("однослово", 1),
    ("", 0),
    ("     ", 0),
])
def test_count_words(text, expected):
    assert count_words(text) == expected