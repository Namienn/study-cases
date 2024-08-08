import Study_Case_1 as sc_i

class Entity():
    attributes = ('STR', 'DEX', 'VIT', 'PER', 'INT', 'CHA', 'LCK', 'WIS', 'ARC', 'PAT')
    
    def __init__(self) -> None:
        """A collection of the fundamental parts for any entity.
        
        Current properties include:
         - name
         - attr_values
         - attr_die
         
         Current methods include:
         - Builder patter for every property
         - roll_stat: Interaction facilitator, returns the power level of a roll
         """
        self.name = ''
        self.attr_values = {
            'STR': 0,
            'DEX': 0,
            'VIT': 0,
            'PER': 0,
            'INT': 0,
            'CHA': 0,
            'LCK': 0,
            'WIS': 0,
            'ARC': 0,
            'PAT': 0
        }
        self.attr_die = {
            'STR': None,
            'DEX': None,
            'VIT': None,
            'PER': None,
            'INT': None,
            'CHA': None,
            'LCK': None,
            'WIS': None,
            'ARC': None,
            'PAT': None
        }
    
    def set_attribute(self, attribute: str, value: int):
        """Builder pattern for attr_values.
        
        The attribute names are as follows:
         - STR: Strength
         - DEX: Dexterity
         - VIT: Vitality
         - PER: Perception
         - INT: Inteligence
         - CHA: Charisma
         - LCK: Luck
         - WIS: Wisdom
         - ARC: Arcane
         - PAT: Patience
         """
        if attribute.upper() not in self.attributes:
            raise ValueError('Invalid Attribute')
        if type(value) != int or value < 0:
            raise TypeError('Attribute must be a non-negative integer')
        
        self.attr_values[attribute.upper()] = value
        return self

    def set_name(self, name: str):
        "Builder pattern for name"
        self.name = name
        return self
    
    @classmethod
    def roll_stat(cls, char, attribute: str, scale: int = 0.1):
        "Rolls a given stat for a given character, according to it's corresponding dice (defaults to d20)."
        if attribute.upper() not in cls.attributes:
            raise ValueError('Invalid Attribute')
        
        dice = char.attr_die[attribute]
        if dice is None:
            dice = sc_i.Dice().set_num_sides(20)
        
        modifier = sc_i.Dice.roll(dice) * scale
        return char.attr_values[attribute] * (modifier+0.4)
    

class Game_Master():
    def __init__(self) -> None:
        pass

    @classmethod
    def clash_stats(cls, entity_1, stat_1, entity_2, stat_2):
        Entity.roll_stat(entity_1, stat_1)

dave = Entity().set_attribute('INT', 7)
print(Entity.roll_stat(dave, 'INT'))

