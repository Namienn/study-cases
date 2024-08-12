import Die_Class as sc_i
import Global_Elements as gl

class Weapon():
    def __init__(self) -> None:
        """A Collection of fundamental parts for any weapon
        
        Current properties (and builder patterns) include:
         - use_attr: The atributes related to weapon usage
         - attr_req: The minimum required level to use the weapon fully
         - dmg_dice: The dice to be used in order to roll damage

        Current methods include:
         - atr_roll: handles the dice rolling for damage
        """
        self.use_attr = None
        self.attr_req = None
        self.dmg_dice = []
    
    def set_use_attr(self, *args: str):
        "Builder pattern for weapon attributes"
        for arg in args:
            if type(arg) is not str:  # Error Handling
                raise TypeError('Parameters must be string objects')
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
    
    def set_dmg_dice(self, *args: sc_i.Die):
        "Builder pattern for damage die"
        for arg in args:
            if type(arg) is not sc_i.Die:  # Error Handling
                raise TypeError('Parameters must be die objects.')
        
        self.dmg_dice = args
        return self
    
    @classmethod
    def atk_roll(cls, weapon):
        "Method for rolling attack dice."
        result = 0
        for die in weapon.dmg_dice:
            result += sc_i.Die.roll(die)
        return result

if __name__ == "__main__":
    stick = Weapon().set_use_attr('Str', 'Vit')

    d4 = sc_i.Die().set_num_sides(4)
    stick.set_dmg_dice(d4, d4, d4, d4)
    
    print(Weapon.atk_roll(stick))
