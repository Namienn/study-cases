from Die_Class import Die
from Weapon_Class import Weapon
import Global_Config as gl
from math import log10

class Entity():
    
    def __init__(self) -> None:
        """A collection of the fundamental parts for any entity.
        
        Current properties (and build patterns) include:
         - name
         - attr_values
         - attr_dice
         - element_mods
         - dmg_type_mods
         
         Current methods include:
         - roll_stat: rolls for stat and handles the math, returning the power level
         - battle_stats: returns a tuple with the entity's conflict stats
         """
        self.name = ''

        self.attr_values = gl.build_attr_values_dict()
        self.attr_dice = gl.build_attr_dice_dict()

        self.element_mods = gl.build_element_modifier_dict()
        self.dmg_type_mods = gl.build_dmg_type_modifier_dict()

    def set_attribute(self, attribute: str, value: int):
        """Builder pattern for attr_values.
        
        Check Global_Elements for current attributes.
        """
        
        gl.check_for_attribute(attribute)  # Error Handling
        if type(value) != int or value < 0:
            raise TypeError('Attribute must be a non-negative integer')
        
        self.attr_values[attribute.upper()] = value
        return self

    def set_name(self, name: str):
        "Builder pattern for name"

        gl.check_for_type(name, str)  # Error Handling

        self.name = name
        return self
    

    def battle_stats(self):
        """ Functionality to be terminated
        
        Conflict stats generator. Returns a List with the following:
        
        - Given Entity
        - Entity's HP: calculate through: 5**log10(VIT) * log10(VIT)*2
        """

        log_vit = log10(self.attr_values['VIT'])
        health_points = int(5**log_vit * log_vit*2)

        return (self, health_points)

    
    @classmethod
    def roll_stat(cls, entity, attribute: str, scale: int = 0.1) -> float:
        """Class method for rolling a given stat for a given entity,
        according to it's corresponding die (defaults to d20). """

        gl.check_for_type(entity, Entity)  # Error Handling
        gl.check_for_attribute(attribute)
        
        die = entity.attr_dice[attribute.upper()]
        if die is None:
            die = Die().set_num_sides(20)
        
        modifier = Die.roll(die) * scale
        return entity.attr_values[attribute.upper()] * (modifier+0.4)
    
    @classmethod 
    def roll_damage(cls, entity, weapon:Weapon) -> int:
        "Handles the math behind rolling for damage."

        gl.check_for_type(entity, Entity)  # Error Handling
        gl.check_for_type(weapon, Weapon)  # Error Handling
        
        base_roll = Weapon.atk_roll(weapon)  # Base roll
        for c, stat in enumerate(weapon.use_attr):
            given_stat = entity.attr_values[stat.upper()]

            multiplier = given_stat/weapon.attr_req[c]  # Calculates how much of the requirement the entity has
            if multiplier < 0.5:  # Caps the minimum at .5, collapsing it to 0 below that 0
                multiplier = 0
            if multiplier > 1.5:  # Caps the maximum at 1.5
                multiplier = 1.5
            base_roll *= multiplier

        return int(base_roll)
