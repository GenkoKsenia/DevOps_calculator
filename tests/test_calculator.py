import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from calculator import add, subtract, multiply, divide

def test_add():
    assert add(2, 3) == 6
    assert add(-1, 1) == 0

def test_subtract():
    assert subtract(5, 3) == 2
    assert subtract(0, 5) == -5

def test_multiply():
    assert multiply(3, 4) == 12
    assert multiply(-2, 3) == -6

def test_divide():
    assert divide(6, 3) == 2
    assert divide(5, 2) == 2.5

def test_divide_by_zero():
    try:
        divide(5, 0)
        assert False, "Expected ValueError"
    except ValueError:
        assert True