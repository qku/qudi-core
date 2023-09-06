import pytest

from qudi.util import units


@pytest.fixture
def scaled():
    return units.ScaledFloat(1234.5)


def test_scale(scaled):
    assert scaled.scale == 'k'


def test_scale_value(scaled):
    assert scaled.scale_val == 1e3


def test_format(scaled):
    assert f'{scaled:.1r}A' == '1.2 kA'


def test_get_unit_prefix_dict():
    assert units.get_unit_prefix_dict()['p'] == 1e-12


def test_create_formatted_output():
    param_dict = {'Rabi frequency': {'value': 123.43, 'error': 0.321, 'unit': 'Hz'},
                  'ODMR contrast': {'value': 2.563423, 'error': 0.523, 'unit': '%'},
                  'Fidelity': {'value': 0.783, 'error': 0.2222, 'unit': ''},
                  'Bin count': {'value': 128, 'error': None, 'unit': ''}}
    assert units.create_formatted_output(param_dict) == ('Rabi frequency: 123.4 ± 0.3 Hz \n'
                                                         'ODMR contrast: 2.6 ± 0.5 % \n'
                                                         'Fidelity: 0.78 ± 0.22  \n'
                                                         'Bin count: 128 \n')


def test_round_to_value_error_1():
    assert units.round_value_to_error(2.05650234, 0.0634) == (2.06, 0.06, 2)


def test_round_to_value_error_2():
    assert units.round_value_to_error(0.34545, 0.19145) == (0.35, 0.19, 2)


def test_round_to_value_error_3():
    assert units.round_value_to_error(239579.23, 1289.234) == (239600.0, 1300.0, -2)


def test_round_to_value_error_4():
    assert units.round_value_to_error(961453, 3789) == (961000, 4000, -3)


def test_round_to_value_error_zero():
    assert units.round_value_to_error(961453, 0) == (961453, 0, -12)


def test_get_relevant_digit_zero():
    assert units.get_relevant_digit(0) == 0


def test_get_relevant_digit_larger_than_one():
    assert units.get_relevant_digit(120) == 2


def test_get_relevant_digit_smaller_than_one():
    assert units.get_relevant_digit(0.005) == -3


def test_si_norm():
    assert units.get_si_norm(3.5e8) == (350, 1e6)
