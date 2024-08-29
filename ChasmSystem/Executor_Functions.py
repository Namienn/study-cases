from .Die_Class import Die
from . import Global_Config as gl

# This file contains the functions utilized by the
# Fetcher class owned by an Ability object.
#
# The functions are referenced through the lambda
# method by the flags, allowing for externalization
# of the utilized functions.

def compose_variables(base_list: list, index_1: int, index_2: int, delete_second_element: bool = False) -> None:
    "Function for multiplying two numbers. Has the option for deleting the second given element"

    gl.check_for_type(base_list[index_1], int, message='list element indexed is the wrong type')
    gl.check_for_type(base_list[index_2], int, message='list element indexed is the wrong type')

    base_list[index_1] = base_list[index_1] * base_list[index_2]
    if delete_second_element:
        base_list[index_2] = None

def roll_die(base_list: list, index_1: int) -> None:
    "Function for rolling a die, redefining it into a number."

    gl.check_for_type(base_list[index_1], Die, message='list element indexed is the wrong type')
    given_die: Die = base_list[index_1]

    base_list[index_1] = Die.roll(given_die)
