from Ability_Class import Ability
import Global_Config as gl

class Aspect():
    def __init__(self) -> None:
        """A Tool for iteratively prototyping entities
        
        Current properties (and builder patterns) include:
        - attr_mods
        - element_mods
        - dmg_type_mods
        - attached_abilities
        
        Current methods include:
        - compose: joins the abilities and composes the modifiers of two Aspects
        - init_multipliers: 
        """

        self.attr_mods = gl.build_attr_modifier_dict()
        self.element_mods = gl.build_element_modifier_dict()
        self.dmg_type_mods = gl.build_dmg_type_modifier_dict()

        self._composition: tuple[Aspect]|tuple = tuple([self])
        self.attached_abilities: list = []
    
    def set_attr_mod(self, attribute: str, value: float):
        "Builder Pattern for attr_mods"

        gl.check_for_attribute(attribute)  # Error Handling
        gl.check_for_type(value, float)
        if value < 1: raise ValueError('Modifier must be greater than one')
        
        self.attr_mods[attribute.upper()] = value
        return self
    
    def set_elem_mod(self, element: str, value: float):

        gl.check_for_element(element)  # Error Handling
        gl.check_for_type(value, float)
        if value < 1: raise ValueError('Modifier must be greater than one')
        
        self.element_mods[element.upper()] = value
        return self
    
    def set_dmg_type_mod(self, dmg_type: str, value: float):
        gl.check_for_dmg_type(dmg_type)  # Error Handling
        gl.check_for_type(value, float)
        if value < 1: raise ValueError('Modifier must be greater than one')
        
        self.dmg_type_mods[dmg_type.upper()] = value
        return self
    
    def set_ability(self, ability: Ability):
        "Builder method for attached_abilities"

        gl.check_for_type(ability, Ability)
        
        self.attached_abilities.append(ability)
        return self

    def init_aspect(self):
        "Feature method for kickstarting composite Aspect properties"

        if len(self._composition) == 1:  # If the called aspect isn't composite, it shouldn't change
            return self

        # Redefining Modifiers

        self.attr_mods = gl.build_attr_modifier_dict()
        self.element_mods = gl.build_element_modifier_dict()
        self.dmg_type_mods = gl.build_dmg_type_modifier_dict()

        # Compounding Base Aspects

        for attr in gl.attributes:
            # Composing Attribute Modifiers
            for aspect in self._composition:
                self.attr_mods[attr] *= aspect.attr_mods[attr]
        
        for elem in gl.elements:
            # Composing Element Modifiers
            for aspect in self._composition:
                self.element_mods[elem] *= aspect.element_mods[elem]
        
        for dmg_type in gl.damage_types:
            # Composing Damage Type Modifiers
            for aspect in self._composition:
                self.dmg_type_mods[dmg_type] *= aspect.dmg_type_mods[dmg_type]
        
        # Redefining Attached Abilities
        
        self.attached_abilities = []

        # Composing Attribute Modifiers
        for aspect in self._composition:
            self.attached_abilities = gl.union_list(self.attached_abilities, aspect.attached_abilities)

        return self

    @classmethod
    def compose(cls, aspect_1, aspect_2):
        "Constructor Method that generates a composite Aspect based on two others"

        gl.check_for_type(aspect_1, Aspect)
        gl.check_for_type(aspect_2, Aspect)
        new_aspect = Aspect()

        # Implementation:
        # This method allows for the emergent creation of more complex
        # Aspects while preventing heritage duplication. Due to the way
        # this method is implemented, it creates a difference between
        # fundamental and composite Aspects.

        new_comp: list[Aspect] = []
        comp_1: tuple = aspect_1._composition
        comp_2: tuple = aspect_2._composition

        new_comp = gl.union_list(comp_1, comp_2)

        new_aspect._composition = tuple(new_comp)
        
        return new_aspect


if __name__ == '__main__':
    metabolizing = Aspect() \
        .set_attr_mod('Vit', 10.0)
    
    breathing = Aspect() \
        .set_attr_mod('Vit', 5.0)

    living = Aspect.compose(metabolizing, breathing)
