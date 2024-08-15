from random import randint
import Global_Config as gl

class Die():
    def __init__(self) -> None:
        """The Ultimate Abstraction of Die

        The currently available properties of this class include:
         - num_sides = Defines the amount of sides the die has
         - modifier = Sets an additive modifier to the die's roll
         - scalar = Sets a multiplicative modifier to the die's roll
        
        The currently available properties of this class include:
         - Single Die Roll
         - Additive Multiple Dice Roll
         - Clashing Multiple Dice Roll
        """

        self.num_sides = 0
        self.modifier = 0
        self.scalar = 1
    
    def set_num_sides(self, num: int):
        " Builder Pattern for num_sides "
        
        gl.check_for_type(num, int)  # Error Handling
        if num < 1:
            raise TypeError("die num_sides must be a strictly positive integer")
        
        self.num_sides = num
        return self
    
    def set_modifier(self, num: int):
        "Builder Pattern for modifier"
        
        gl.check_for_type(num, int)  # Error Handling
        
        self.modifier = num
        return self
    
    def set_scalar(self, num:int):
        "Builder Pattern for scalar"
        
        gl.check_for_type(num, int)  # Error Handling
        if num < 1:
            raise TypeError("die scalar must be a strictly positive integer")
        
        self.scalar = num
        return self
    
    @staticmethod
    def roll(die) -> int:
        "Class method for single die roll."

        return randint(1, die.num_sides) * die.scalar + die.modifier
    
    @classmethod
    def sum_roll(cls, *dice) -> int:
        "Class method for additive multiple dice roll."
        
        final_sum = 0
        for die in dice:
            gl.check_for_type(die, Die, 'Dice list includes non-die elements')  # Error Handling
            
            final_sum += cls.roll(die)

        return final_sum
    
    @classmethod
    def clash_roll(cls, *dice) -> list[list]:
        """Class method for clashing multiple dice roll.

        Returns a list with the die indexes ordered from highest to lowest, each in a sublist.
        In case of a tie, the indexes share the same sublist."""

        rolls = []
        for die in dice:
            gl.check_for_type(die, Die, 'Dice list includes non-die elements')  # Error Handling
            
            rolls.append(cls.roll(die))
        
        # Sorting Method:
        # Step 1: Find max value and it's index
        # Step 2: Check if the index's value is the same
            # If not, create a new list with the found index inside
            # If yes, append the found index with the last list available, tracking found value
        # Step 3: Track current max value for next iteration
        # Step 4: Turn found index's list value to -1
        # Loop steps 1-4 until max list value is measured at -1
        # - - -
        # due to the implementation of the loop, it adds an extra unnecessary element
        # at the end of each return list. that's why it's chopped at the last value.

        win_order = []
        win_values = []
        previous_max = 0
        while previous_max >= 0:  # Begin Sorting
            max_value = max(rolls)  # Step 1
            max_index = rolls.index(max_value)  # Step 1

            if max_value == previous_max:  # Step 2
                win_order[-1].append(max_index)
            else:
                win_order.append([max_index])
                win_values.append(max_value)  # Step 2
            
            previous_max = max_value  # Step 3
            rolls[max_index] = -1  # Step 4
        
        return win_order[:-1], win_values[:-1]
