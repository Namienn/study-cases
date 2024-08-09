# This file contains the constants to be used
# throughout the program.  It also allows for
# the implementation of functions to standardize
# different values.

attributes = ('STR', 'DEX', 'VIT', 'PER', 'INT', 'CHA', 'LCK', 'WIS', 'ARC', 'PAT')  # Attribute names

def build_attr_values_dict():
    "Constructs the Attribute Values Dict based on the current set of attributes."
    frame_dict = {}
    for attr in attributes:
        frame_dict[attr] = 1
    
    return frame_dict

def build_attr_dice_dict():
    "Constructs the Attribute Die Dict based on the current set of attributes."
    frame_dict = {}
    for attr in attributes:
        frame_dict[attr] = None
    
    return frame_dict