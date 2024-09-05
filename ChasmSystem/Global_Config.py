# This file contains the constants to be used
# throughout the program.  It also allows for
# the implementation of functions to standardize
# different values.

# Attribute Standardization

attributes = ('STR', 'DEX', 'VIT', 'PER', 'INT', 'CHA', 'LCK', 'WIS', 'ARC', 'PAT')  # Attribute names

def build_attr_values_dict() -> dict:
    "Constructs the Attribute Values Dict based on the current set of attributes."
    frame_dict = {}
    for attr in attributes:
        frame_dict[attr] = 1
    
    return frame_dict

def build_attr_dice_dict() -> dict:
    "Constructs the Attribute Die Dict based on the current set of attributes."
    frame_dict = {}
    for attr in attributes:
        frame_dict[attr] = None
    
    return frame_dict


# Element Standardization

elements = ('FIRE', 'WATER', 'EARTH', 'AIR', 'LIGHT', 'DARKNESS', 'ORDER', 'CHAOS', 'NATURE', 'NEUTRAL')  # Element names
damage_types = ('SLICE', 'PIERCE', 'SLASH', 'BLUNT')  # Damage Type names

def build_element_modifier_dict() -> dict:
    "Constructs the element modifier dict based on the current set of elements"
    frame_dict = {}
    for el in elements:
        frame_dict[el] = 1
    
    return frame_dict

def build_dmg_type_modifier_dict() -> dict:
    "Constructs the damage type modifier dict based on the current set of elements"
    frame_dict = {}
    for typ in damage_types:
        frame_dict[typ] = 1

    return frame_dict

def build_attr_modifier_dict() -> dict:
    "Constucts the Attribute Modifiers dict based on the current set of attributes"

    # Redundancy is allowed for readability and
    # possible later reimplementation purposes

    return build_attr_values_dict()


# Common Error Handling Routines

def check_for_type(element, type_check, message: str = 'Parameter type invalid') -> None:
    "Function to confirm if a given element is of a specified type"

    if type(element) is not type_check:
        raise TypeError(message + f' - {type(element)} != {type_check}')

def check_in_config(element: str, config_check, message: str = 'Parameter given does not fit the required standard') -> None:
    "Abstract Function to handle standardizes variables."

    check_for_type(element, str)
    if element.upper() not in config_check:
        raise ValueError(message)

def check_for_attribute(element: str, message: str = 'Parameter is not a valid attribute') -> None:
    "Function to confirm if a given string qualifies as an attribute"

    # Redundancy is allowed for readability and
    # possible later reimplementation purposes
    
    return check_in_config(element, attributes, message)

def check_for_element(element: str, message: str = 'Parameter is not a valid element') -> None:
    "Function to confirm if a given string qualifies as an element"

    # Redundancy is allowed for readability and
    # possible later reimplementation purposes
    
    return check_in_config(element, elements, message)

def check_for_dmg_type(element: str, message: str = 'Parameter is not a valid damage type') -> None:
    "Function to confirm if a given string qualifies as a damage type"

    # Redundancy is allowed for readability and
    # possible later reimplementation purposes

    return check_in_config(element, damage_types, message)


# Complex Methods

def union_list(iter_1: list|tuple, iter_2: list|tuple) -> list:
    "Funtion to ease the finding and removal of repetition while joining two iterators"
    union_list = []
    el_list = []
    el_list.extend (iter_1)
    el_list.extend (iter_2)

    for el in el_list:
        if el not in union_list:
            union_list.append(el)

    return union_list

def data_slot_form(method, parameters: tuple):
    "Function to create single input methods out of complex ones based on given parameters"
    return lambda data: method(data, *parameters)

def dict_from_double_iter(keys_iter: list|tuple, values_iter: list|tuple) -> dict:
    "Function to create a dict based off of the values of two iterable elements"
    if len(keys_iter) != len(values_iter): raise KeyError('Given keys and values iters do not match lengths')

    return_dict = dict()
    for c in range(len(keys_iter)):
        return_dict[keys_iter[c]] = values_iter[c]
    
    return return_dict