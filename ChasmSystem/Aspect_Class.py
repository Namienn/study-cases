from Die_Class import Die
import Global_Config as gl

class Aspect():
    def __init__(self) -> None:
        """A Tool for iteratively prototyping entities
        
        Current properties (and builder patterns) include:
        - attr_mod_values
        - elem_mod_values
        - dmg_type_mod_values
        
        Current methods include:
        - compose: joins the abilities and composes the modifiers of two Aspects
        """

        self.attr_mods = gl.build_attr_modifier_dict()
        self.element_mods = gl.build_element_modifier_dict()
        self.dmg_type_mods = gl.build_dmg_type_modifier_dict()

        self.composition: tuple[Aspect]|tuple = tuple([self])
        self.attached_abilities = None
    
    def set_attr_mod(self, attribute, value: float):

        gl.check_for_attribute(attribute)  # Error Handling
        gl.check_for_type(value, float)
        if value < 1: raise ValueError('Modifier must be greater than one')
        
        self.attr_mods[attribute.upper()] = value
        return self
    
    def set_elem_mod(self, attribute, value: float):

        gl.check_for_element(attribute)  # Error Handling
        gl.check_for_type(value, float)
        if value < 1: raise ValueError('Modifier must be greater than one')
        
        self.element_mods[attribute.upper()] = value
        return self
    
    def set_dmg_type_mod(self, attribute, value: float):

        gl.check_for_dmg_type(attribute)  # Error Handling
        gl.check_for_type(value, float)
        if value < 1: raise ValueError('Modifier must be greater than one')
        
        self.dmg_type_mods[attribute.upper()] = value
        return self
    
    def compose(self, aspect):
        gl.check_for_type(aspect, Aspect)
        new_aspect = Aspect()

        new_comp: list[Aspect] = []
        comp_1: tuple = self.composition
        comp_2: tuple = aspect.composition

        new_comp = gl.union_list(comp_1, comp_2)

        new_aspect.composition = tuple(new_comp)
        
        return new_aspect

    def init_multipliers(self):
        "Feature method for redefining Aspect properties"

        self.attr_mods = gl.build_attr_modifier_dict()
        self.element_mods = gl.build_element_modifier_dict()
        self.dmg_type_mods = gl.build_dmg_type_modifier_dict()

        for attr in gl.attributes:
            # Composing Attribute Modifiers
            for aspect in self.composition:
                self.attr_mods[attr] *= aspect.attr_mods[attr]
        
        for elem in gl.elements:
            # Composing Element Modifiers
            for aspect in self.composition:
                self.element_mods[elem] *= aspect.element_mods[elem]
        
        for dmg_type in gl.damage_types:
            # Composing Damage Type Modifiers
            for aspect in self.composition:
                self.dmg_type_mods[dmg_type] *= aspect.dmg_type_mods[dmg_type]
        
        return self


if __name__ == '__main__':
    metabolizing = Aspect() \
        .set_attr_mod('Vit', 10.0)
    
    breathing = Aspect() \
        .set_attr_mod('Vit', 5.0)

    living = Aspect.compose(metabolizing, breathing)
