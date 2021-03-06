import pytest


def my_sum(a, b):
    return a + b


# Sequential
@pytest.mark.dummytest
@pytest.mark.parametrize("a,b,s", [
    (1, 1, 2),
    (1, 2, 3),
    (2, 2, 4),
])
def test_param_1(a, b, s):
    assert my_sum(a, b) == s


# Combinatorial
@pytest.mark.dummytest
@pytest.mark.parametrize("a", [1, 2])
@pytest.mark.parametrize("b", [11, 12, 13])
@pytest.mark.parametrize("s", [101, 102, 103, 104])
def test_param_2(a, b, s):
    assert my_sum(a, b) < s


@pytest.mark.dummytest
@pytest.mark.webtest
def test_webtest_1():
    assert True


@pytest.mark.dummytest
@pytest.mark.webtest
def test_webtest_2():
    assert True


@pytest.mark.dummytest
@pytest.mark.smoketest
def test_smoketest_1():
    assert True


@pytest.mark.dummytest
@pytest.mark.smoketest
def test_smoketest_2():
    assert True
