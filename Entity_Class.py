import Die_Class as sc_i
import Global_Elements as gl
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
        self.attr_values = gl.build_attr_values_dict()
        self.attr_dice = gl.build_attr_dice_dict()

    def set_attribute(self, attribute: str, value: int):
        """Builder pattern for attr_values.
        
        Check Global_Elements for current attributes.
         """
        
        if attribute.upper() not in gl.attributes:  # Error Handling
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
        "Rolls a given stat for a given character, according to it's corresponding die (defaults to d20)."
        if attribute.upper() not in gl.attributes:  # Error Handling
            raise ValueError('Invalid Attribute')
        
        die = char.attr_dice[attribute.upper()]  # upper() method drops the case-sensitiveness
        if die is None:
            die = sc_i.Die().set_num_sides(20)
        
        modifier = sc_i.Die.roll(die) * scale
        return char.attr_values[attribute.upper()] * (modifier+0.4)