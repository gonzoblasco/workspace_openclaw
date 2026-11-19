import pytest

from calc import divide

@pytest.mark.parametrize("a,b,expected", [(4, 2, 2.0), (9, 3, 3.0)])
def test_divide_valid(a, b, expected):
    assert divide(a, b) == expected

def test_divide_by_zero_raises():
    with pytest.raises(ValueError):
        divide(1, 0)
