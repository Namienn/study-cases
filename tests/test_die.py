import pytest

import sys
sys.path.append('/home/thomas/Documents/VSCode Paste/study_cases')

from ChasmSystem import Die

@pytest.fixture()
def d4():
    return Die() \
        .set_num_sides(4)

@pytest.fixture()
def scaled_d4():
    return Die() \
        .set_num_sides(4) \
        .set_scalar(10)

@pytest.fixture()
def modified_d4():
    return Die() \
        .set_num_sides(4) \
        .set_modifier(5)

@pytest.fixture
def mixed_d4():
    return Die() \
        .set_num_sides(4) \
        .set_modifier(5) \
        .set_scalar(5)

def test_init(d4, scaled_d4, modified_d4, mixed_d4):
    assert type(d4) is Die
    assert type(scaled_d4) is Die
    assert type(modified_d4) is Die
    assert type(mixed_d4) is Die