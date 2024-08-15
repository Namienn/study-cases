from Die_Class import Die
import Global_Config as gl

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
        self.attr_use: tuple[str] = None
        self.attr_req: tuple[int] = None

        self.dmg_dice: tuple[Die] = []

        self.dmg_type = None
    
    def set_attr_use(self, *args: str):
        "Builder pattern for weapon attributes"
        for arg in args:
            gl.check_for_attribute(arg)
        
        self.attr_use = args
        return self
    
    def set_attr_req(self, *args: int):
        "Builder pattern for attribute requirements"

        if len(args) != len(self.attr_use):
            raise IndexError('Amount of numbers given doesn\'t match the number of weapon attributes')
        for arg in args:
            gl.check_for_type(arg, int)
            
        self.attr_req = args
        return self
    
    def set_dmg_dice(self, *args: Die):
        "Builder pattern for damage die"
        for arg in args:
            gl.check_for_type(arg, Die)
        
        self.dmg_dice = args
        return self
    
    def set_dmg_type(self, given_type: str):
        "Builder pattern for damage type"
        gl.check_for_dmg_type(given_type)
        
        self.dmg_type = given_type
        return self

    @classmethod
    def atk_roll(cls, weapon) -> int:
        "Class method for rolling attack dice."

        gl.check_for_type(weapon, Weapon)

        result = 0
        for die in weapon.dmg_dice:
            result += Die.roll(die)
        return result


if __name__ == "__main__":
    d4 = Die() \
        .set_num_sides(4)
    
    stick = Weapon() \
        .set_attr_use('Str', 'Vit') \
        .set_dmg_dice(d4, d4, d4, d4)
    
    print(Weapon.atk_roll(stick))
