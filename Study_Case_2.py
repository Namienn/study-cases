import Study_Case_1 as sc_i

class Character():
    def __init__(self) -> None:
        self.name = ''
        self.attributes = {
            'STR': 0,
            'DEX': 0,
            'VIT': 0,
            'PER': 0,
            'INT': 0,
            'CHA': 0,
            'LCK': 0,
            'WIS': 0,
            'ARC': 0,
            'PAT': 0,
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
            'PAT': None,
        }
    
    def set_attribute(self, attribute: str, value: int):
        if attribute.upper() not in self.attributes.keys():
            raise ValueError('Invalid Attribute')
        if type(value) != int or value < 0:
            raise TypeError('Attribute must be a non-negative integer')
        
        self.attributes[attribute.upper()] = value
        return self

    def set_name(self, name: str):
        self.name = name
        return self
    
    @classmethod
    def roll_stat(cls, attribute: str):
        sc_i.Dice().set_num_sides(20)
    

dave = Character().set_attribute('INT', 7)

