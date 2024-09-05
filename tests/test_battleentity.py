import pytest

from pathlib import Path

from tests.test_entity import base_ability
this_directory = Path(__file__).parent.parent

import sys
sys.path.append(str(this_directory))

from ChasmSystem import Entity, BattleEntity, Aspect, Weapon, Die


@pytest.fixture()
def entity():
    return Entity() \
        .set_attribute('Vit', 100) \
        .set_attribute('Pat', 220) \
        .set_attribute('Arc', 130) \
        .set_attribute('Int', 330) \

@pytest.fixture()
def aspect():
    metabolizing = Aspect() \
        .set_attr_mod('Vit', 1.5) \
    
    breathing = Aspect() \
        .set_attr_mod('Pat', 3.0) \

    return Aspect.compose(metabolizing, breathing)

@pytest.fixture()
def weapon():
    d4 = Die() \
        .set_num_sides(4)
    
    return Weapon() \
        .set_attr_use('Str', 'Vit') \
        .set_attr_req(50, 75) \
        .set_dmg_dice(d4, d4, d4, d4)


def test_from_entity(entity):
    assert BattleEntity.from_entity(entity)

def test_start_up(entity):
    base_b_ent = BattleEntity.from_entity(entity)
    assert base_b_ent.hp == 0
    assert base_b_ent.mp == 0

    BattleEntity.start_up(base_b_ent)
    assert base_b_ent.hp == 117
    assert base_b_ent.mp == 141

def test_delta_hp(entity):
    base_b_ent = BattleEntity.from_entity(entity)
    BattleEntity.start_up(base_b_ent)

    assert base_b_ent.hp == 117
    BattleEntity.delta_hp(base_b_ent, 30)
    assert base_b_ent.hp == 147

def test_roll_damage(entity, weapon):
    base_b_entity = BattleEntity.from_entity(entity)

    assert type(BattleEntity.roll_damage(base_b_entity, weapon)) is int