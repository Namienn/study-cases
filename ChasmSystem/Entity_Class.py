from Die_Class import Die
from Weapon_Class import Weapon
import Global_Config as gl
from math import log10

class Entity():
    
    def __init__(self) -> None:
        """A collection of the fundamental parts for any entity.
        
        Current properties (and build patterns) include:
         - id_name
         - attr_values
         - attr_dice
         
         Current methods include:
         - roll_stat: rolls for stat and handles the math, returning the power level
         - battle_stats: returns a tuple with the entity's conflict stats
         """
        self.id_name = ''

        self.attr_values: dict[str, int] = gl.build_attr_values_dict()
        self.attr_dice: dict[str, Die] = gl.build_attr_dice_dict()

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

        self.id_name = name
        return self
    
    @classmethod
    def roll_stat(cls, entity, attribute: str, scale: int = 0.1) -> int:
        """Class method for rolling a given stat for a given entity,
        according to it's corresponding die (defaults to d20). """

        gl.check_for_type(entity, Entity)  # Error Handling
        gl.check_for_attribute(attribute)
        
        die = entity.attr_dice[attribute.upper()]
        if die is None:
            die = Die().set_num_sides(20)
        
        modifier = Die.roll(die) * scale
        return int(entity.attr_values[attribute.upper()] * (modifier+0.4))


class BattleEntity(Entity):
    def __init__(self) -> None:
        """The spotlight of encounters
        
        Current properties include:
        - hp: Health Points
        - mp: Mana Points
        - attr_mods
        - element_mods
        - dmg_type_mods
        - abilities
        
        Current methods include:
        - delta_hp: Adds a given value to the entity's health points
        - clash_stats: Calculates the winner of a clash between attributes.
        - roll_damage: Calculates the damage output of a weapon yielded by an entity"""
        super().__init__()

        self.hp = 0
        self.mp = 0

        self.attr_mods: dict[str, float] = gl.build_attr_modifier_dict()
        self.element_mods: dict[str, float] = gl.build_element_modifier_dict()
        self.dmg_type_mods: dict[str, float] = gl.build_dmg_type_modifier_dict()

        self.abilities = {}

    @classmethod
    def from_entity(cls, entity: Entity):
        gl.check_for_type(entity, Entity)

        new_b_entity = cls()
        new_b_entity.attr_values = entity.attr_values
        new_b_entity.attr_dice = entity.attr_dice

        return new_b_entity
    
    @classmethod
    def start_up(cls, b_entity) -> None:
        log_vit = log10(b_entity.attr_values['VIT'])
        log_pat = log10(b_entity.attr_values['PAT'])
        b_entity.hp = int(5**log_vit * log_pat*2)

        log_arc = log10(b_entity.attr_values['ARC'])
        log_int = log10(b_entity.attr_values['INT'])
        b_entity.mp = int(4**log_arc*log_int*3)
    
    @classmethod
    def roll_stat(cls, entity, attribute: str, scale: int = 0.1) -> int:
        """Class method for rolling a given stat for a given entity,
        according to it's corresponding die (defaults to d20). """

        gl.check_for_type(entity, BattleEntity)  # Error Handling
        gl.check_for_attribute(attribute)
        
        die = entity.attr_dice[attribute.upper()]
        if die is None:
            die = Die().set_num_sides(20)
        
        modifier = Die.roll(die) * scale
        modified_attr = entity.attr_values[attribute.upper()] * entity.attr_mods[attribute.upper()]
        return int(modified_attr * (modifier+0.4))

    @classmethod
    def delta_hp(cls, b_entity, value: int) -> None:
        b_entity.hp += value

    @classmethod
    def clash_stats(cls, b_entities: dict) -> list[list]:
        """Class method for stat conflict settling. 
        
        Receives a dict with the keys as the entities and the
        values as string with the attribute they'll roll
        
        Returns the index of the winner and the roll result."""
        
        rolls = []
        for entry in b_entities.items():

            current_entity = entry[0]
            roll_attribute = entry[1]

            gl.check_for_attribute(roll_attribute)  # Error Handling
            gl.check_for_type(current_entity, BattleEntity)
            
            rolls.append(BattleEntity.roll_stat(current_entity, roll_attribute))
        
        # Code snippet copied over from Die class
        # Check over there for better explanation of the
        # base functionality
        
        win_order = []
        win_values = []
        previous_max = 0
        while previous_max >= 0:  # Begin Sorting
            max_value = max(rolls)  # Step 1
            max_index = rolls.index(max_value)  # Step 1

            if max_value == previous_max:  # Step 2
                win_order[-1].append(max_index)
            else:
                win_order.append([max_index])
                win_values.append(max_value)  # Step 2
            
            previous_max = max_value  # Step 3
            rolls[max_index] = -1  # Step 4
        
        return win_order[:-1], win_values[:-1]
    
    @classmethod 
    def roll_damage(cls, entity, weapon:Weapon) -> int:
        "Handles the math behind rolling for damage."

        gl.check_for_type(entity, BattleEntity)  # Error Handling
        gl.check_for_type(weapon, Weapon)  # Error Handling
        
        base_roll = Weapon.atk_roll(weapon)  # Base roll
        for c, stat in enumerate(weapon.attr_use):
            given_stat = entity.attr_values[stat.upper()]

            multiplier = given_stat/weapon.attr_req[c]  # Calculates how much of the requirement the entity has
            if multiplier < 0.5:  # Caps the minimum at .5, collapsing it to 0 below that 0
                multiplier = 0
            if multiplier > 1.5:  # Caps the maximum at 1.5
                multiplier = 1.5
            base_roll *= multiplier

        return int(base_roll)


if __name__ == '__main__':
    dave = Entity() \
        .set_attribute('Vit', 350) \
        .set_attribute('Pat', 220) \
        .set_attribute('Arc', 130) \
        .set_attribute('Int', 330)
    f_dave = BattleEntity.from_entity(dave)

    joe = Entity() \
        .set_attribute('Vit', 90) \
        .set_attribute('Pat', 120) \
        .set_attribute('Arc', 640) \
        .set_attribute('Int', 440)
    f_joe = BattleEntity.from_entity(joe)

    BattleEntity.start_up(f_dave)
    print(f_dave.hp, f_dave.mp)

    print(BattleEntity.clash_stats({f_dave: 'Vit', f_joe: 'Arc'}))
