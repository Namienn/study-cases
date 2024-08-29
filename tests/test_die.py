import pytest

from pathlib import Path
this_directory = Path(__file__).parent.parent

print(this_directory)

import sys
sys.path.append(str(this_directory))

from ChasmSystem import Die

@pytest.fixture()
def d4():
    "Fixture for test die"

    return Die() \
        .set_num_sides(4)

@pytest.mark.parametrize(
        "num_sides, modifier, scalar",
        [
            (6, 0, 1),  # Regular die
            (1, 0, 1),  # One-Sided die
            (4, 1, 1),  # Modified die
            (4,-2, 1),  # Negative Modified die
            (5, 0, 3),  # Scaled die
            (16,8, 2)   # Mixed Input die
        ]
)
def test_init(num_sides: int, modifier: int, scalar: int) -> None:
    "Test for multiple different die builder parameters"

    assert type(Die().set_num_sides(num_sides).set_modifier(modifier).set_scalar(scalar)) is Die

def test_roll(d4: Die) -> None:
    "Test for die roll staticmethod"

    assert type(Die.roll(d4)) is int

def test_sum_roll(d4: Die) -> None:
    "Test for die sum_roll staticmethod"

    assert type(Die.sum_roll(d4, d4, d4)) is int

def test_clash_roll(d4: Die) -> None:
    "Test for die clash_roll staticmethod"

    assert type(Die.clash_roll(d4, d4, d4)) is tuple
    classification_list, die_rolls = Die.clash_roll(d4, d4, d4)
    
    assert type(classification_list) is list
    assert type(classification_list[0]) is list
    assert type(classification_list[0][0]) is int

    assert type(die_rolls) is list
    assert type(die_rolls[0]) is int

@pytest.mark.parametrize(
        "num_sides, modifier, scalar",
        [
            (6.0, 0, 1),  # Wrong due to num_sides being float
            (4, 1.5, 1),  # Wrong due to modifier being float
            (5, 0, 3.6),  # Wrong due to scalar being float
        ]
)
def test_invalid_input(num_sides, modifier, scalar):
    "Test for invalid type input on builder methods"

    with pytest.raises(TypeError):
        Die().set_num_sides(num_sides).set_modifier(modifier).set_scalar(scalar)

@pytest.mark.parametrize(
        "num_sides, modifier, scalar",
        [
            (0, 0, 1),   # Wrong due to num-sides set to 0
            (-1, 1, 1),  # Wrong due to num-sides being negative
            (16,8, 0),   # Wrong due to scalar set to 0
            (4, 0, -2)   # Wrong due to scalar set to negative
        ]
)
def test_out_of_bounds_input(num_sides, modifier, scalar):
    "Test for out of bounds input on builder methods"

    with pytest.raises(ValueError):
        Die().set_num_sides(num_sides).set_modifier(modifier).set_scalar(scalar)