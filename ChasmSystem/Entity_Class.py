from Aspect_Class import Aspect
from Die_Class import Die
from Weapon_Class import Weapon
from Ability_Class import Ability
import Global_Config as gl
from math import log10

class Entity():
    
    def __init__(self) -> None:
        """A collection of the fundamental parts for any entity.
        
        Current properties (and build patterns) include:
         - id_name
         - attributes
         - attr_dice
         - aspect
         - abilities
         
         Current methods include:
         - roll_stat: rolls for stat and handles the math, returning the power level
         - clash_stats: rolls for stats in multiple entities and handles the math, returning the power level
         - roll
         """
        self.id_name = ''

        self._attr_values: dict[str, int] = gl.build_attr_values_dict()
        self.attr_dice: dict[str, Die] = gl.build_attr_dice_dict()

        self._attr_mods: dict[str, float] = gl.build_attr_modifier_dict()

        self.aspect: Aspect = Aspect()

    @property
    def attributes(self):
        "Property method for fetching Attributes"

        attr_dict = {}
        for attr in gl.attributes:
            attr_dict[attr] = int(self._attr_values[attr] * self._attr_mods[attr])
        
        return attr_dict
    
    @property
    def abilities(self):
        "Property method for fetching Abilities"

        return self.aspect.attached_abilities

    def set_attribute(self, attribute: str, value: int):
        """Builder pattern for attr_values.
        
        Check Global_Elements for current attributes.
        """
        
        gl.check_for_attribute(attribute)  # Error Handling
        if type(value) != int or value < 0:
            raise TypeError('Attribute must be a non-negative integer')
        
        self._attr_values[attribute.upper()] = value
        return self

    def set_name(self, name: str):
        "Builder pattern for name"

        gl.check_for_type(name, str)  # Error Handling

        self.id_name = name
        return self

    def add_aspects(self, *args: Aspect):
        "Builder pattern for aspects"

        new_aspect = self.aspect
        for arg in args:
            gl.check_for_type(arg, Aspect)
            new_aspect = Aspect.compose(new_aspect, arg)
        
        self.aspect = new_aspect.init_aspect()
        return self.init_mods()

    def init_mods(self):
        "Feature method for fetching data from Aspect"
        self._attr_mods = self.aspect.attr_mods

        return self

    def return_data(self):
        "Method for exporting an entity's data"

        return self.attributes, self.attr_dice, self.aspect

    @staticmethod
    def roll_stat(entity, attribute: str, scale: float = 0.1) -> int:
        """staticmethod for rolling a given stat for a given entity,
        according to it's corresponding die (defaults to d20). """

        gl.check_for_attribute(attribute)
        
        die = entity.attr_dice[attribute.upper()]
        if die is None:
            die = Die().set_num_sides(20)
        modifier = Die.roll(die) * scale

        base_value = entity.attributes[attribute.upper()]  # Attribute Modifier is applied here
        return int(base_value * (modifier+0.4))
    
    @staticmethod
    def clash_stats(b_entities: dict) -> tuple[list, list]:
        """staticmethod for stat conflict settling. 
        
        Receives a dict with the keys as the entities and the
        values as string with the attribute they'll roll
        
        Returns the index of the winner and the roll result."""
        
        rolls = []
        for entry in b_entities.items():

            current_entity = entry[0]
            roll_attribute = entry[1]

            gl.check_for_attribute(roll_attribute)  # Error Handling
            
            rolls.append(Entity.roll_stat(current_entity, roll_attribute))
        
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
    
    @staticmethod
    def engage_ability(entity, ability: Ability):
        "Method for calling an ability within the entity's skillset"

        if ability not in entity.abilities:
            raise IndexError("Entity does not posess given ability")
        
        entity_data = entity.return_data()
        
        return ability.engage(entity_data)
        

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

        self.element_mods: dict[str, float] = gl.build_element_modifier_dict()
        self.dmg_type_mods: dict[str, float] = gl.build_dmg_type_modifier_dict()

    def init_mods(self):
        "Feature method for fetching data from Aspect"
        self._attr_mods = self.aspect.attr_mods
        self.element_mods = self.aspect.element_mods
        self.dmg_type_mods = self.aspect.dmg_type_mods

        return self

    @classmethod
    def from_entity(cls, entity: Entity):
        "BattleEntity Constructor that uses an Entity object as foundation"
        gl.check_for_type(entity, Entity)

        new_b_entity = cls()
        new_b_entity._attr_values = entity._attr_values
        new_b_entity.attr_dice = entity.attr_dice

        new_b_entity.aspect = entity.aspect

        return new_b_entity.init_mods()
    
    @staticmethod
    def start_up(b_entity) -> None:
        "Method to generate the BattleEntity's stats"
        log_vit = log10(b_entity.attributes['VIT'])
        log_pat = log10(b_entity.attributes['PAT'])
        b_entity.hp = int(5**log_vit * log_pat*2)

        log_arc = log10(b_entity.attributes['ARC'])
        log_int = log10(b_entity.attributes['INT'])
        b_entity.mp = int(4**log_arc * log_int*3)

    @staticmethod
    def delta_hp(b_entity, value: int) -> None:
        "Method to handle any adjacent processes of modifying an BattleEntity's HP (mostly placeholder for now)"
        b_entity.hp += value
    
    @staticmethod 
    def roll_damage(entity, weapon:Weapon) -> int:
        "Handles the math behind rolling for damage."

        gl.check_for_type(entity, BattleEntity)  # Error Handling
        gl.check_for_type(weapon, Weapon)  # Error Handling
        
        base_roll = Weapon.atk_roll(weapon)  # Base roll
        for c, stat in enumerate(weapon.attr_use):
            given_stat = entity.attributes[stat.upper()]

            multiplier = given_stat/weapon.attr_req[c]  # Calculates how much of the requirement the entity has
            if multiplier < 0.5:  # Caps the minimum at .5, collapsing it to 0 below that 0
                multiplier = 0
            if multiplier > 1.5:  # Caps the maximum at 1.5
                multiplier = 1.5
            base_roll *= multiplier

        return int(base_roll)


if __name__ == '__main__':
    walking = Ability(FETCH_STATS=('Vit', 'Pat'), ADD_NUMBERS=(2, 5)) \
        .add_command('Compose', (1, 2, True)) \
        .add_command('Compose', (0, 2, True))
    
    metabolizing = Aspect() \
        .set_attr_mod('Vit', 1.5) \
        .set_ability(walking)
    
    breathing = Aspect() \
        .set_attr_mod('Vit', 8.0)

    living = Aspect.compose(metabolizing, breathing)

    dave = Entity() \
        .set_attribute('Vit', 350) \
        .set_attribute('Pat', 220) \
        .set_attribute('Arc', 130) \
        .set_attribute('Int', 330) \
        .add_aspects(living)
    f_dave = BattleEntity.from_entity(dave)

    joe = Entity() \
        .set_attribute('Vit', 90) \
        .set_attribute('Pat', 120) \
        .set_attribute('Arc', 640) \
        .set_attribute('Int', 440) \
        .add_aspects(metabolizing, breathing)
    f_joe = BattleEntity.from_entity(joe)

    print(f_dave.hp, f_dave.mp)
    BattleEntity.start_up(f_dave)
    print(f_dave.hp, f_dave.mp)


    print(Entity.clash_stats({dave: 'Vit', joe: 'Arc'}))
    print(Entity.engage_ability(dave, walking))


