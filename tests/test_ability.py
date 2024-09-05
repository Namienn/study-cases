import pytest

from pathlib import Path
this_directory = Path(__file__).parent.parent

import sys
sys.path.append(str(this_directory))

from ChasmSystem import Die, Entity, Ability
from ChasmSystem.Ability_Class import Fetcher, Executor

@pytest.fixture()
def ability():
    "Fixture for test ability"

    return Ability(FETCH_STATS=('Vit', 'Str'), ADD_NUMBERS=(2,)) \
        .add_command('COMPOSE', (0, 2)) \
        .add_command('COMPOSE', (1, 2, True))

@pytest.fixture()
def entity():
    "Fixture for test entity"
    
    return Entity() \
    .set_attribute('Vit', 10) \
    .set_attribute('Str', 10)

@pytest.fixture()
def die():
    "Fixture for test die"

    return Die().set_num_sides(4)

@pytest.mark.parametrize(
        "flags",
        [
            {},  # No Flags
            {'FETCH_STATS': ('Str')},  # FETCH_STATS flag
            {'ADD_NUMBERS': (2, )}  # ADD_NUMBERS flag
        ]
)
def test_init(flags: dict):
    "Testing for multiple init parameters"

    assert Ability(**flags)

def test_requirements(ability: Ability):
    "Testing for parameters property method"

    reqs = ability.parameters
    assert type(reqs) is dict

def test_pŕocess(ability: Ability):
    "Testing for process property method"

    proc = ability.process
    assert type(proc) is tuple

def test_engage(entity: Entity, ability: Ability):
    "Testing for ability engage method"
    ent_data = entity.return_data()
    assert ability.engage(ent_data) == [20, 20]

def test_fetcher_flag_call():
    "Testing for individual calling of each flag in Fetcher class"

    for flag in Fetcher.parameter_flags.keys():
        assert callable(Fetcher.parameter_flags[flag]) is True

def test_executor_flag_call():
    "Testing for individual calling of each flag in Executor class"

    for flag in Executor.parameter_flags.keys():
        assert callable(Executor.parameter_flags[flag]) is True

def test_invalid_flag_call():
    "Testing for invalid flag calls within Fetcher and Executor class"

    assert Fetcher.check_for_parameter_flag('Banans') is False
    assert Executor.check_for_parameter_flag('Banans') is False