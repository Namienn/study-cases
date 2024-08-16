from Die_Class import Die
import Global_Config as gl

class Aspect():
    def __init__(self) -> None:
        self.attr_mod_values = gl.build_attr_modifier_dict()
        self.elem_mod_values = gl.build_element_modifier_dict()
        self.dmg_type_mod_values = gl.build_dmg_type_modifier_dict()

        self.attached_abilities = None
    
    def set_attr_mod(self, attribute, value):

        gl.check_for_attribute(attribute)  # Error Handling
        gl.check_for_type(value, int)
        if value < 1: raise ValueError('Modifier must be greater than one')
        
        self.attr_mod_values[attribute.upper()] = value
        return self
    
    def set_elem_mod(self, attribute, value):

        gl.check_for_element(attribute)  # Error Handling
        gl.check_for_type(value, int)
        if value < 1: raise ValueError('Modifier must be greater than one')
        
        self.elem_mod_values[attribute.upper()] = value
        return self
    
    def set_dmg_type_mod(self, attribute, value):

        gl.check_for_dmg_type(attribute)  # Error Handling
        gl.check_for_type(value, int)
        if value < 1: raise ValueError('Modifier must be greater than one')
        
        self.dmg_type_mod_values[attribute.upper()] = value
        return self
    
    @classmethod
    def compose(cls, aspect_1, aspect_2):
        new_aspect = Aspect()

        for attr in gl.attributes:
            composed_mod = aspect_1.attr_mod_values[attr] * aspect_2.attr_mod_values[attr]
            new_aspect.set_attr_mod(attr, composed_mod)
        
        for elem in gl.elements:
            composed_mod = aspect_1.elem_mod_values[elem] * aspect_2.elem_mod_values[elem]
            new_aspect.set_elem_mod(elem, composed_mod)
        
        for dmg_type in gl.damage_types:
            composed_mod = aspect_1.dmg_type_mod_values[dmg_type] * aspect_2.dmg_type_mod_values[dmg_type]
            new_aspect.set_dmg_type_mod(dmg_type, composed_mod)
        
        return new_aspect


if __name__ == '__main__':
    metabolizing = Aspect() \
        .set_attr_mod('Vit', 10)
    
    breathing = Aspect() \
        .set_attr_mod('Vit', 5)

    living = Aspect.compose(metabolizing, breathing)