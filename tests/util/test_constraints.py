import pytest

from qudi.util.constraints import ScalarConstraint

DEFAULT = 0.5
BOUNDS = (0, 1)
INCREMENT = 0.1
ENFORCE_INT = False
CHECKER_FAIL = 0.7


def checker(x):
    return x != CHECKER_FAIL


@pytest.fixture
def constraint():
    return ScalarConstraint(default=DEFAULT, bounds=BOUNDS,
                            increment=INCREMENT, enforce_int=ENFORCE_INT,
                            checker=checker)


@pytest.fixture
def constraint_enforce_int():
    return ScalarConstraint(default=int(DEFAULT), bounds=BOUNDS,
                            enforce_int=True)


def test_bounds(constraint):
    assert constraint.bounds == BOUNDS


def test_minimum(constraint):
    assert constraint.minimum == min(BOUNDS)


def test_maximum(constraint):
    assert constraint.maximum == max(BOUNDS)


def test_default(constraint):
    assert constraint.default == DEFAULT


def test_increment(constraint):
    assert constraint.increment == INCREMENT


def test_enforce_int(constraint):
    assert constraint.enforce_int == ENFORCE_INT


def test_check_fail_type(constraint):
    with pytest.raises(TypeError):
        constraint.check_value_type('yo')


def test_check_fail_type_enforce_int(constraint_enforce_int):
    with pytest.raises(TypeError):
        constraint_enforce_int.check_value_type(0.1)


def test_check_fail_range(constraint):
    value = 2 * max(BOUNDS)
    with pytest.raises(ValueError):
        constraint.check_value_range(2 * value)


def test_check_fail_custom(constraint):
    with pytest.raises(ValueError):
        constraint.check_custom(CHECKER_FAIL)


def test_check_pass(constraint):
    assert constraint.is_valid(DEFAULT)


def test_clip(constraint):
    value = min(BOUNDS) - 1
    assert constraint.clip(value) == min(BOUNDS)


def test_repr(constraint):
    assert f'{DEFAULT}' in constraint.__repr__()
