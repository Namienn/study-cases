import pytest

from pathlib import Path
this_directory = Path(__file__).parent.parent

import sys
sys.path.append(str(this_directory))

from ChasmSystem import Die, Weapon

@pytest.fixture()
def weapon():
    d4 = Die() \
        .set_num_sides(4)
    
    return Weapon() \
        .set_attr_use('Str', 'Vit') \
        .set_attr_req(50, 75) \
        .set_dmg_dice(d4, d4, d4, d4)

@pytest.mark.parametrize(
        "attr_use",
        [
            (),  # None test
            ('VIT',),  # Single attr test
            ('VIT', 'DEX'),  # Multiple attr test
        ]
)
def test_set_attr_use(attr_use):
    base_weapon = Weapon()

    assert base_weapon.set_attr_use(*attr_use) is base_weapon
    assert base_weapon.attr_use == attr_use

def test_attr_use_duplication():
    base_weapon = Weapon().set_attr_use('Vit', 'Vit')
    
    assert base_weapon.attr_use == ('VIT',)

def test_invalid_attr_use_input():
    with pytest.raises(ValueError):
        Weapon().set_attr_use("bananas")

@pytest.mark.parametrize(
        "attr_use, attr_req",
        [
            ((),()),  # None test
            (('Vit',), (10,)),  # Single attr test
            (('Vit', 'Dex'), (10, 15)),  # Multiple attr test
        ]
)
def test_set_attr_req(attr_use, attr_req):
    base_weapon = Weapon().set_attr_use(*attr_use)

    assert base_weapon.set_attr_req(*attr_req) is base_weapon
    assert base_weapon.attr_req == attr_req

def test_invalid_req_len():
    with pytest.raises(IndexError):
        Weapon().set_attr_use("Vit").set_attr_req(10, 51)

def test_attributes_property(weapon: Weapon):
    assert weapon.attributes == {'STR': 50, 'VIT': 75}

def test_set_dmg_type():
    base_weapon = Weapon()

    assert base_weapon.set_dmg_type('SLICE') is base_weapon

@pytest.mark.parametrize(
        "dmg_type",
        [
            None,  # None test
            ('a', 'b'),  # Invalid input type test
            'Bananas',  # Invalid dmg type test
        ]
)
def test_invalid_dmg_type_input(dmg_type):
    with pytest.raises((TypeError, ValueError)):
        Weapon().set_dmg_type(dmg_type)

def test_atk_roll(weapon):
    assert Weapon.atk_roll(weapon)