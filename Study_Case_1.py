from random import randint

class Dice():
    def __init__(self) -> None:
        """The Ultimate Abstraction of Dice

        The currently available properties of this class include:
         - num_sides = Defines the amount of sides the dice has
         - modifier = Sets an additive modifier to the dice's roll
         - scalar = Sets a multiplicative modifier to the dice's roll
        
        The currently available properties of this class include:
         - Single Dice Roll
         - Additive Multiple Die Roll
         - Clashing Multiple Die Roll
        """

        self.num_sides = 0
        self.modifier = 0
        self.scalar = 1
    
    def set_num_sides(self, num: int):
        " Builder Pattern of self.num_sides "
        if type(num) != type(1):
            raise TypeError("dice num_sides must be a strictly positive integer")
        if num < 1:
            raise TypeError("dice num_sides must be a strictly positive integer")
        
        self.num_sides = num
        return self
    
    def set_modifier(self, num: int):
        "Builder Pattern of self.modifier"
        if type(num) != type(1):
            raise TypeError("dice num_sides must be an integer")
        self.modifier = num
        return self
    
    def set_scalar(self, num:int):
        if type(num) != type(1):
            raise TypeError("dice num_sides must be a strictly positive integer")
        if num < 1:
            raise TypeError("dice num_sides must be a strictly positive integer")
        
        self.scalar = num
        return self
    
    @staticmethod
    def roll(dice):
        "Single dice roll. Returns a single number"
        return (randint(1, dice.num_sides) + dice.modifier) * dice.scalar
    
    @classmethod
    def sum_roll(cls, die: list):
        "Additive multiple die roll. Returns a single number, sum of all rolled die"
        final_sum = 0
        for dice in die:
            if type(dice) != cls:
                raise TypeError('Dice list given includes non-dice elements')
            
            final_sum += cls.roll(dice)

        return final_sum
    
    @classmethod
    def clash_roll(cls, die: list):
        """Clashing multiple die roll. 
        Returns a list with the die indexes ordered from highest to lowest, each in a sublist.
        In case of a tie, the indexes share the same sublist."""
        rolls = []
        for dice in die:
            if type(dice) != cls:
                raise TypeError('Dice list given includes non-dice elements')
            
            rolls.append(cls.roll(dice))
        
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
        # at the end of each return list, that's why it's chopped at the last value.

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


if __name__ == "__main__":
    pass