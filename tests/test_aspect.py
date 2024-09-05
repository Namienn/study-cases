from email.mime import base
import pytest

from pathlib import Path
this_directory = Path(__file__).parent.parent

import sys
sys.path.append(str(this_directory))

from ChasmSystem import Ability, Aspect

@pytest.fixture()
def aspect_1():
    return Aspect() \
        .set_attr_mod('Vit', 10.0)

@pytest.fixture()
def aspect_2():
    return Aspect() \
        .set_attr_mod('Vit', 5.0)

@pytest.fixture()
def ability():
    return Ability()

@pytest.mark.parametrize(
        "attr_mods",
        [
            {},  # None test
            {'Vit': 2},  # Single attr test
            {'Vit': 0.5, 'Dex': 1.5},  # Multiple attr test
            {'Vit': 1.5, 'Vit': 0}   # Redundant definition test
        ]
)
def test_attr_init(attr_mods: dict):
    base_aspect = Aspect()

    for item in attr_mods.items():
        assert base_aspect.set_attr_mod(item[0], item[1]) is base_aspect

@pytest.mark.parametrize(
        "elem_mods",
        [
            {},  # None test
            {'Fire': 3},  # Single attr test
            {'Fire': 0.7, 'Water': 1.2},  # Multiple attr test
            {'Fire': 0.7, 'Fire': 0}   # Redundant definition test
        ]
)
def test_elem_init(elem_mods: dict):
    base_aspect = Aspect()

    for item in elem_mods.items():
        assert base_aspect.set_elem_mod(item[0], item[1]) is base_aspect

@pytest.mark.parametrize(
        "dmg_type_mods",
        [
            {},  # None test
            {'Slice': 0.4},  # Single attr test
            {'Slice': 0.4, 'Slash': 2},  # Multiple attr test
            {'Slice': 1.6, 'Slice': 0}   # Redundant definition test
        ]
)
def test_dmg_mod_init(dmg_type_mods: dict):
    base_aspect = Aspect()

    for item in dmg_type_mods.items():
        assert base_aspect.set_dmg_type_mod(item[0], item[1]) is base_aspect

def test_ability_init(ability: Ability):
    base_aspect = Aspect()

    assert base_aspect.set_ability(ability) is base_aspect
    assert base_aspect.attached_abilities == [ability]

def test_compose(aspect_1, aspect_2: Aspect, ability: Ability):
    aspect_2.set_ability(ability)

    composed_aspect = Aspect.compose(aspect_1, aspect_2)
    assert type(composed_aspect) is Aspect
    assert composed_aspect.attached_abilities == [ability]

def test_init(aspect_1, aspect_2):
    base_aspect = Aspect()

    assert base_aspect.init_aspect() is base_aspect
    assert base_aspect.attr_mods['VIT'] == 1

    compose_aspect = Aspect.compose(aspect_1, aspect_2)
    assert compose_aspect.init_aspect() is compose_aspect
    assert compose_aspect.attr_mods['VIT'] == 50
