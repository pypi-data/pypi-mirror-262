import pytest

from sample_project_ivi import calculate_mean, print_mean


def test_calculate_mean_normal_operation():
    assert calculate_mean([1, 2, 3, 4, 5]) == 3.0
    assert calculate_mean([1.0, 2.0, 3.0, 4.0, 5.0]) == 3.0
    assert calculate_mean([1, 2.0, 3, 4.0, 5]) == 3.0


def test_calculate_mean_empty_list():
    with pytest.raises(ZeroDivisionError):
        calculate_mean([])


def test_calculate_mean_non_list_input():
    with pytest.raises(ValueError) as e:
        calculate_mean("not a list")
    assert str(e.value) == "Input must be a list."


def test_calculate_mean_non_number_in_list():
    with pytest.raises(ValueError) as e:
        calculate_mean([1, 2, 3, "not a number", 5])
    assert str(e.value) == "not a number is not a number."


# capfd is a built-in pytest fixture that captures stdout and stderr
def test_print_mean_normal_operation(capfd):
    print_mean([1, 2, 3, 4, 5])
    out, err = capfd.readouterr()
    assert out == "The average is: 3.0\n"
    assert err == ""


def test_print_mean_empty_list(capfd):
    with pytest.raises(ZeroDivisionError):
        print_mean([])
    out, err = capfd.readouterr()
    assert out == ""
    assert err == ""


def test_print_mean_non_list_input(capfd):
    with pytest.raises(ValueError) as e:
        print_mean("not a list")
    out, err = capfd.readouterr()
    assert out == ""
    assert err == ""
    assert str(e.value) == "Input must be a list."


def test_print_mean_non_number_in_list(capfd):
    with pytest.raises(ValueError) as e:
        print_mean([1, 2, 3, "not a number", 5])
    out, err = capfd.readouterr()
    assert out == ""
    assert err == ""
    assert str(e.value) == "not a number is not a number."
