""" This is a sample module. """

from typing import List, Union


def calculate_mean(numbers: List[Union[int, float]]) -> float:
    """
    Calculate the mean of a list of numbers.

    Parameters
    ----------
    numbers : List[Union[int, float]]
        A list of numbers.

    Returns
    -------
    float
        The mean of the numbers.

    Raises
    ------
    ValueError
        If the input is not a list of numbers.
    """

    if not isinstance(numbers, list):
        raise ValueError("Input must be a list.")
    # ensure all elements are numbers
    for number in numbers:
        if not isinstance(number, (int, float)):
            raise ValueError(f"{number} is not a number.")

    total = sum(numbers)
    average = total / len(numbers)
    return average


def print_mean(numbers: List[Union[int, float]]) -> None:
    """
    Print the mean of a list of numbers.

    Parameters
    ----------
    numbers : List[Union[int, float]]
        A list of numbers.
    """
    print("The average is:", calculate_mean(numbers))
