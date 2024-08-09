import Study_Case_1 as sc_i
import Study_Case_2 as sc_ii
import Global_Elements as globals

class Weapon():
    def __init__(self) -> None:
        self.use_attr = None
        self.dmg_dice = None
    
    def set_use_attr(self, *args):
        for arg in args:
            if type(arg) is not str:  # Error Handling
                raise TypeError('Parameters must be strings separated by commas')
            if arg.upper() not in globals.attributes:
                raise ValueError('Weapon parameters must be valid Entity attributes')
        
        self.use_attr = args
        return self
    
    def set_dmg_dice(self, dice: sc_i.Dice):
        if type(dice) is not sc_i.Dice:  # Error Handling
            raise TypeError('Parameter must be Dice object')
        
        self.dmg_dice = dice
        return self


stick = Weapon().set_use_attr('Str', 'Vit')

d4 = sc_i.Dice().set_num_sides(4)
stick.set_dmg_dice(d4)

print(stick.dmg_dice)
