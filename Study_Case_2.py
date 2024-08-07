import Study_Case_1 as sc_i

class Character():
    attributes = ('STR', 'DEX', 'VIT', 'PER', 'INT', 'CHA', 'LCK', 'WIS', 'ARC', 'PAT')
    
    def __init__(self) -> None:
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
        if attribute.upper() not in self.attributes:
            raise ValueError('Invalid Attribute')
        if type(value) != int or value < 0:
            raise TypeError('Attribute must be a non-negative integer')
        
        self.attr_values[attribute.upper()] = value
        return self

    def set_name(self, name: str):
        self.name = name
        return self
    
    @classmethod
    def roll_stat(cls, char, attribute: str, scale: int = 0.1):
        if attribute.upper() not in cls.attributes:
            raise ValueError('Invalid Attribute')
        
        dice = char.attr_die[attribute]
        if dice is None:
            dice = sc_i.Dice().set_num_sides(20)
        
        modifier = sc_i.Dice.roll(dice) * scale
        return char.attr_values[attribute] * (modifier+0.4)
    

dave = Character().set_attribute('INT', 7)
print(Character.roll_stat(dave, 'INT'))

