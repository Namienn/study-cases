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


class BattleEntity(Entity):
    def __init__(self) -> None:
        super().__init__()

        log_vit = log10(self.attr_values['VIT'])
        log_pat = log10(self.attr_values['PAT'])
        self.hp = int(5**log_vit * log_pat*2)

        log_arc = log10(self.attr_values['ARC'])
        log_int = log10(self.attr_values['INT'])
        self.mp = int(4**log_arc*log_int*3)

        self.attr_mods = gl.build_attr_modifier_dict()
        self.element_mods = gl.build_element_modifier_dict()
        self.dmg_type_mods = gl.build_dmg_type_modifier_dict()

        self.abilities = {}
    
    @classmethod
    def delta_hp(cls, b_entity, value: int) -> None:
        b_entity.hp += value

    @classmethod
    def clash_stats(cls, entity_1, stat_1:str, entity_2, stat_2:str) -> tuple:
        """Class method for stat conflict settling. 
        
        Receives two sets of Entity, str.
        
        Returns the index of the winner and the roll result."""

        gl.check_for_type(entity_1, BattleEntity)
        gl.check_for_attribute(stat_1)
        gl.check_for_type(entity_2, BattleEntity)
        gl.check_for_attribute(stat_2)

        roll_1 = Entity.roll_stat(entity_1, stat_1)
        roll_2 = Entity.roll_stat(entity_2, stat_2)

        if roll_1 > roll_2:
            return (0, roll_1)
        return (1, roll_2)
    
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

