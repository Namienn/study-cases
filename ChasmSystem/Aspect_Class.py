from .Die_Class import Die
from . import Global_Config as gl

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

        gl.check_for_attribute(attribute)  # Error Handling
        gl.check_for_type(value, int)
        if value < 1: raise ValueError('Modifier must be greater than one')
        
        self.elem_mod_values[attribute.upper()] = value
        return self
    
    def set_dmg_type_mod(self, attribute, value):

        gl.check_for_attribute(attribute)  # Error Handling
        gl.check_for_type(value, int)
        if value < 1: raise ValueError('Modifier must be greater than one')
        
        self.dmg_type_mod_values[attribute.upper()] = value
        return self