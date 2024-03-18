from src.calculator_meluzx.calculator_meluzx import Calculator
import pytest

cal = Calculator()


def main():
    """Calls all the test functions"""
    test_positive()
    test_negative()
    test_zeros()
    test_str()


def test_positive():
    """Tests cases with positive numbers"""
    assert cal.reset() == 0
    assert cal.add(26) == 26
    assert cal.subtract(6) == 20
    assert cal.multiply(2) == 40
    assert cal.divide(4) == 10
    assert cal.root(3) == 2.15


def test_negative():
    """Tests cases with negative numbers"""
    assert cal.reset() == 0
    assert cal.add(-10) == -10
    assert cal.subtract(-5) == -5
    assert cal.multiply(-3) == 15
    assert cal.divide(-5) == -3
    assert cal.root(-2) == "Answer is imaginary number"


def test_zeros():
    """Tests cases with zeros"""
    assert cal.reset() == 0
    assert cal.add(0) == 0
    assert cal.subtract(0) == 0
    assert cal.multiply(0) == 0
    assert cal.divide(0) == "Division by 0 not possible"
    assert cal.root(0) == "Invalid"


def test_str():
    """Tests cases with string variables"""
    with pytest.raises(TypeError):
        cal.add("a")
        cal.subtract("10")
        cal.multiply("a")
        cal.divide("a")
        cal.root("1")


"""Calling main function"""
if __name__ == "__main__":
    main()
