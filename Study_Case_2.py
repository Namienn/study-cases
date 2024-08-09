import Study_Case_1 as sc_i
import Global_Elements as globals
from math import log10

class Entity():
    
    def __init__(self) -> None:
        """A collection of the fundamental parts for any entity.
        
        Current properties (and build patterns) include:
         - name
         - attr_values
         - attr_die
         
         Current methods include:
         - roll_stat: rolls for stat and handles the math, returning the power level
         - battle_stats: returns a tuple with the entity's conflict stats
         """
        self.name = ''
        self.attr_values = globals.build_attr_values_dict()
        self.attr_die = globals.build_attr_dice_dict()

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
        
        if attribute.upper() not in globals.attributes:  # Error Handling
            raise ValueError('Invalid Attribute')
        if type(value) != int or value < 0:
            raise TypeError('Attribute must be a non-negative integer')
        
        self.attr_values[attribute.upper()] = value
        return self

    def set_name(self, name: str):
        "Builder pattern for name"

        self.name = name
        return self
    

    def battle_stats(self):
        """Conflict stats generator. Returns a List with the following:
        
        - Given Entity
        - Entity's HP: calculate through: 5**log10(VIT) * log10(VIT)*2
        """

        log_vit = log10(self.attr_values['VIT'])
        health_points = int(5**log_vit * log_vit*2)

        return (self, health_points)

    
    @classmethod
    def roll_stat(cls, char, attribute: str, scale: int = 0.1):
        "Rolls a given stat for a given character, according to it's corresponding dice (defaults to d20)."
        if attribute.upper() not in globals.attributes:  # Error Handling
            raise ValueError('Invalid Attribute')
        
        dice = char.attr_die[attribute.upper()]  # upper() method drops the case-sensitiveness
        if dice is None:
            dice = sc_i.Dice().set_num_sides(20)
        
        modifier = sc_i.Dice.roll(dice) * scale
        return char.attr_values[attribute.upper()] * (modifier+0.4)
    

class Game_Master():
    def __init__(self) -> None:
        """The mediator between entities within a conflict
        
        Current properties (and build patterns) include:
        - active_entities
        
        Current methods include:
        - clash_stats: settles a conflict between two attributes of two entities
        """
        self.active_entities = {}

    def add_entities(self, ent_list: tuple):
        "Builder pattern for active_entities"
        for entity in ent_list:
            if type(entity) is not Entity:  # Error Handling
                raise TypeError('Entity list contains non-entity elements')
            
            battle_stats = entity.battle_stats()
            self.active_entities[battle_stats[0]] = [battle_stats[1]]
        
        return self
    
    def delta_HP(self, entity, value):
        "Facade for altering HP value. Adds given value to an active entity"

        if entity not in self.active_entities.keys():  # Error Handling
            raise TypeError('Given object doesn\'t allign with active entities')

        self.active_entities[entity][0] += value


    @classmethod
    def clash_stats(cls, entity_1: Entity, stat_1:str, entity_2:Entity, stat_2:str):
        "Stat conflict settler. calls for stat rolls, returning the index of the winner and the roll result."
        if type(entity_1) is not Entity or type(entity_2) is not Entity:  # Error Handling
            raise TypeError('Non-entity element passed as entity')

        roll_1 = Entity.roll_stat(entity_1, stat_1)
        roll_2 = Entity.roll_stat(entity_2, stat_2)

        if roll_1 > roll_2:
            return (0, roll_1)
        return (1, roll_2)


if __name__ == "__main__":
    dave = Entity().set_attribute('Vit', 3156)
    joe = Entity().set_attribute('Str', 2865)

    game = Game_Master().add_entities([dave, joe])

    print(game.clash_stats(dave, 'Vit', joe, 'Str'))
    game.delta_HP(dave, -50)
    print(game.active_entities[dave])
