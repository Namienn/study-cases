import Study_Case_1 as sc_i
import Global_Elements as gl

class Weapon():
    def __init__(self) -> None:
        """A Collection of fundamental parts for any weapon
        
        Current properties (and builder patterns) include:
         - use_attr: The atributes related to weapon usage
         - attr_req: The minimum required level to use the weapon fully
         - dmg_die: The die to be used in order to roll damage

        Current methods include:
         - atr_roll: handles the die rolling for damage
        """
        self.use_attr = None
        self.attr_req = None
        self.dmg_die = None
    
    def set_use_attr(self, *args: str):
        "Builder pattern for weapon attributes"
        for arg in args:
            if type(arg) is not str:  # Error Handling
                raise TypeError('Parameters must be strings separated by commas')
            if arg.upper() not in gl.attributes:
                raise ValueError('Weapon parameters must be valid Entity attributes')
        
        self.use_attr = args
        return self
    
    def set_attr_req(self, *args: int):
        "Builder pattern for attribute requirements"
        if len(args) != len(self.use_attr):
            raise IndexError('Amount of numbers given doesn\'t match the number of weapon attributes')
        
        for arg in args:
            if type(arg) is not int:
                raise TypeError('Requirement must be an integer')
            
        self.attr_req = args
        return self
    
    def set_dmg_die(self, die: sc_i.Die):
        "Builder pattern for damage die"
        if type(die) is not sc_i.Die:  # Error Handling
            raise TypeError('Parameter must be Die object')
        
        self.dmg_die = die
        return self
    
    @classmethod
    def atk_roll(cls, weapon):
        "Method for rolling attack die."
        return sc_i.Die.roll(weapon.dmg_die)

if __name__ == "__main__":
    stick = Weapon().set_use_attr('Str', 'Vit')

    d4 = sc_i.Die().set_num_sides(4)
    stick.set_dmg_die(d4)

    print(stick.dmg_die)
