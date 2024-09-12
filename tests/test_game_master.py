import pytest

from pathlib import Path
this_directory = Path(__file__).parent.parent

import sys
sys.path.append(str(this_directory))

from ChasmSystem import Entity, BattleEntity, Aspect, Weapon, Die, GameMaster


@pytest.fixture()
def entity():
    return Entity() \
        .set_attribute('Vit', 100) \
        .set_attribute('Pat', 220) \
        .set_attribute('Arc', 130) \
        .set_attribute('Int', 330) \
        .set_name('Dave')

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


def test_add_entity(entity):
    game_master = GameMaster()

    assert type((game_master).add_entities(entity)) is GameMaster
    assert type(game_master.active_entities['Dave']) is BattleEntity

def test_start_engagement(entity):
    game_master = GameMaster().add_entities(entity)

    assert game_master.active_entities['Dave'].hp == 0
    game_master.start_engagement()
    assert game_master.active_entities['Dave'].hp != 0

"""
if __name__ == '__main__':
    from Weapon_Class import Weapon
    from Die_Class import Die

    d4 = Die().set_num_sides(4)

    dave = Entity() \
        .set_attribute('Vit', 350) \
        .set_attribute('Pat', 220) \
        .set_attribute('Arc', 130) \
        .set_attribute('Int', 330) \
        .set_name('dave')
    
    wand = Weapon() \
        .set_attr_use('Int', 'Pat') \
        .set_attr_req(100, 100) \
        .set_dmg_dice(d4, d4, d4)

    game = GameMaster().add_entities(dave)
    
    print(game.active_entities['dave'].hp, end=' ')
    game.start_engagement()
    print(game.active_entities['dave'].hp)

    print(BattleEntity.roll_damage(game.active_entities['dave'], wand))"""