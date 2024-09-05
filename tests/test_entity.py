import pytest

from pathlib import Path
this_directory = Path(__file__).parent.parent

import sys
sys.path.append(str(this_directory))

from ChasmSystem import Entity, Aspect, Ability

def base_ability():
    return Ability(FETCH_STATS=('Vit', 'Pat'), ADD_NUMBERS=(2, 5)) \
        .add_command('Compose', (1, 2, True)) \
        .add_command('Compose', (0, 2, True))

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
def ability():
    return base_ability()

@pytest.mark.parametrize(
        "attr_set",
        [
            {},  # None test
            {'VIT': 50},  # Single attr test
            {'VIT': 50, 'DEX': 75},  # Multiple attr test
            {'VIT': 50, 'VIT': 75},  # Repeated attr test
        ]
)
def test_set_attribute(attr_set: dict[str, int]):
    base_entity = Entity()

    for attr in attr_set.items():
        assert base_entity.set_attribute(attr[0], attr[1])
        assert base_entity.attributes[attr[0]] == attr_set[attr[0]]

@pytest.mark.parametrize(
        "attr_name, attr_value",
        [
            ('VIT', -1),  # Negative test
            ('bananas', 20),  # Invalid attribute test
            (12, 'Vit')  # Invalid typing test
        ]
)
def test_invalid_set_attribute(attr_name, attr_value):
    with pytest.raises((TypeError, ValueError)):
        Entity().set_attribute(attr_name, attr_value)

def test_set_name():
    base_entity = Entity()

    assert base_entity.set_name('Bananas') is base_entity

def test_add_aspects(aspect: Aspect):
    base_entity = Entity()

    assert base_entity.add_aspects(aspect) is base_entity

def test_ability_inheritance(ability: Ability):
    base_aspect = Aspect().set_ability(ability)
    base_entity = Entity().add_aspects(base_aspect)

    assert base_entity.abilities == [ability]

def test_attr_modification(entity: Entity, aspect: Aspect):
    entity.add_aspects(aspect)

    assert entity.attributes['VIT'] == 150
    assert entity.attributes['PAT'] == 660

def test_roll_stat(entity: Entity):
    assert type(Entity.roll_stat(entity, 'VIT')) is int

def test_clash_stats():
    entity_1 = Entity().set_attribute('Vit', 100)
    entity_2 = Entity().set_attribute('Pat', 100)
    entity_3 = Entity().set_attribute('Arc', 100)
    clash_dict = {entity_1: 'Vit', entity_2: 'Pat', entity_3: 'Arc'}
    
    assert type(Entity.clash_stats(clash_dict)) is tuple
    classification_list, die_rolls = Entity.clash_stats(clash_dict)
    
    assert type(classification_list) is list
    assert type(classification_list[0]) is list
    assert type(classification_list[0][0]) is int

    assert type(die_rolls) is list
    assert type(die_rolls[0]) is int

def test_engage_ability(ability):
    base_aspect = Aspect().set_ability(ability)
    base_entity = Entity().add_aspects(base_aspect)

    assert Entity.engage_ability(base_entity, ability) == [5, 2]

def test_invalid_ability(entity, ability):
    with pytest.raises(IndexError):
        Entity.engage_ability(entity, ability)
