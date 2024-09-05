import pytest

from pathlib import Path
this_directory = Path(__file__).parent.parent

import sys
sys.path.append(str(this_directory))

from ChasmSystem import Die
from ChasmSystem import Executor_Functions as ef

def test_compose_variables():
    "Testing compose_variables function"
    
    base_list = [10, 10]
    assert ef.compose_variables(base_list, 0, 1) is None
    assert base_list == [100, 10]

    assert ef.compose_variables(base_list, 0, 1, True) is None
    assert base_list == [1000, None]

def test_roll_die():
    "Testing roll_die function"

    base_list = [Die().set_num_sides(4)]
    assert ef.roll_die(base_list, 0) is None
    assert type(base_list[0]) is int
