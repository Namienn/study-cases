from . import Global_Config as gl
from . import Fetcher_Functions as ff
from . import Executor_Functions as ef

class Ability():
    def __init__(self, **kwargs: tuple) -> None:
        """An Abstraction of Skillset
        
        The current attributes include:
         - fetch_args
         - fetcher
         - parameters
         - commands
         - executor
        
        The current methods include:
        - engage: Kickstarts the execution of a preconfigured ability
        """
        self.fetch_args: dict[str, tuple] = kwargs
        self.fetcher: Fetcher = Fetcher()

        self.commands: dict[str, tuple] = {}
        self.executor: Executor = Executor()
    
    @property
    def parameters(self) -> dict:
        "Property method for generating the ability's required parameters"

        parameters: dict = self.fetcher \
            .set_flags(**self.fetch_args) \
            .return_reqs()
        
        return parameters
    
    @property
    def process(self):
        "Property method for generating the ability's execution procedure"

        process: tuple = Executor() \
            .set_commands(**self.commands) \
            .return_proc()
        
        return process
    
    def add_command(self, flag: str, instructions: tuple):
        "Builder method for commands. Configures the ability's process"

        command = f'{flag.upper()}/{len(self.commands)}'
        self.commands[command] = instructions

        return self

    def engage(self, ent_data: tuple):
        "Method for automatic execution of the ability, fetching the required data and processing it"

        # Data Fetching Process
        fetch_list = []
        for req in self.parameters.values():
            retrieved_data = req(ent_data)
            fetch_list.extend(retrieved_data)

        # Automatic Execution Process
        for step in self.process:
            step(fetch_list)
            for _ in range(fetch_list.count(None)):
                fetch_list.remove(None)
        return(fetch_list)



class Fetcher():
    def __init__(self) -> None:
        """Data Fetching module of Ability
        
        current properties include:
         - flags
         - parameter_flags
        
        current methods include:
         - return_reqs: outputs the functions for data fetching based on flags
         - check_for_parameter_flag: identifies Fetcher flags
        """
        self.flags: dict[str, tuple]
    
    def set_flags(self, **kwargs: tuple):
        "Builder method for flags"

        flags: dict = {}

        for arg in kwargs.items():
            if self.check_for_parameter_flag(arg[0]):
                flags[arg[0]] = arg[1]
        
        self.flags = flags
        return self
    
    def return_reqs(self) -> dict:
        "Method for outputting the functions responsible for fetching the correct data"

        requirements = {}
        for flag in self.flags.items():
            requirements[flag[0]] = (self.parameter_flags[flag[0]](flag[1]))
        
        return requirements

    # Fetch Parameter Flags

    @classmethod
    def check_for_parameter_flag(cls, element: str, message: str = 'Parameter is not a valid flag') -> bool:
        "Function to confirm if a given string qualifies as a parameter flag"

        try:
            gl.check_in_config(element, cls.parameter_flags.keys(), message)
        except ValueError:
            return False
        else:
            return True

    parameter_flags = {
            'FETCH_STATS': lambda args: gl.data_slot_form(ff.fetch_attribute, args),
            'ADD_NUMBERS': lambda args: gl.data_slot_form(ff.add_numbers, args)
            }


class Executor():
    def __init__(self) -> None:
        """Data Manipulation module of Ability
        
        current properties include:
         - commands
         - parameter_flags
        
        current methods include:
         - return_proc: outputs the functions for data manipulation based on commands
         - check_for_parameter_flag: identifies Executor flags
        """
        self.commands: dict[str, tuple] = {}

    def set_commands(self, **kwargs: tuple):
        "Builder method for commands"

        commands: dict = {}

        for c, arg in enumerate(kwargs.items()):
            flag = arg[0].split('/')[0]
            if self.check_for_parameter_flag(flag.upper()):
                commands[arg[0]] = arg[1]
        
        self.commands = commands
        return self
    
    def return_proc(self) -> tuple:
        "Method for outputting the functions responsible for manipulating the data"
        process = []
        for command in self.commands.items():
            flag = command[0].split('/')[0]
            process.append(self.parameter_flags[flag.upper()](command[1]))
        
        return tuple(process)

    # Execute Parameter Flags
    
    @classmethod
    def check_for_parameter_flag(cls, element: str, message: str = 'Parameter is not a valid flag') -> bool:
        "Function to confirm if a given string qualifies as a parameter flag"

        try:
            gl.check_in_config(element, cls.parameter_flags.keys(), message)
        except ValueError:
            return False
        else:
            return True

    parameter_flags = {
            'ROLL_DIE': lambda args: gl.data_slot_form(ef.roll_die, args),
            'COMPOSE': lambda args: gl.data_slot_form(ef.compose_variables, args)
            }
    

if __name__ == '__main__':
    from Entity_Class import Entity
    from Die_Class import Die

    walking = Ability(FETCH_STATS=('Vit', 'Str', 'Str'), ADD_NUMBERS=(2, 5))

    d4 = Die().set_num_sides(4)
    test_list = [5, d4]
    die_roll = Executor.parameter_flags['ROLL_DIE'](tuple([1]))
    die_roll(test_list)
    print(test_list)

    walking.add_command('Compose', (1, 2))
    walking.add_command('Compose', (0, 2))
    process = walking.process

    entity = Entity() \
        .set_attribute('Vit', 10) \
        .set_attribute('Str', 15)
    
    print(walking.engage(entity.return_data()))