from spb import MB
from sympy.core.numbers import Float

from gym_cas import regression_exp, regression_poly, regression_power


def test_linear():
    f, p = regression_poly([1, 2, 3], [3, 6, 12], 1, show=False, return_plot=True)  # type: ignore
    assert callable(f)
    assert type(f(2.0)) == Float
    assert isinstance(p, MB)


def test_poly():
    f, p = regression_poly([1, 2, 3, 4], [3, 6, 12, 4], 2, show=False, return_plot=True)  # type: ignore
    f = regression_poly([1, 2, 3, 4], [3, 6, 12, 4], 2, show=False)
    assert callable(f)
    assert type(f(2.0)) == Float
    assert isinstance(p, MB)


def test_power():
    f, p = regression_power([1, 2, 3], [3, 6, 12], show=False, return_plot=True)  # type: ignore
    f = regression_power([1, 2, 3], [3, 6, 12], show=False)
    assert callable(f)
    assert type(f(2.0)) == Float
    assert isinstance(p, MB)


def test_exp():
    f, r2, p = regression_exp([1, 2, 3], [3, 6, 12], return_r2=True, return_plot=True, show=False)  # type: ignore
    f, r2 = regression_exp([1, 2, 3], [3, 6, 12], return_r2=True, show=False)  # type: ignore
    f = regression_exp([1, 2, 3], [3, 6, 12], show=False)
    assert callable(f)
    assert type(f(2.0)) == Float
    assert isinstance(r2, float)
    assert isinstance(p, MB)
