from Die_Class import Die
import Global_Config as gl

class Ability():
    def __init__(self, **kwargs: tuple) -> None:
        self.fetch_args: dict[str, tuple] = kwargs
        self.fetcher: Fetcher = Fetcher()

        self.commands: dict[str, tuple] = {}
        self.executor: Executor = Executor()
    
    @property
    def parameters(self) -> dict:
        parameters: dict = self.fetcher \
            .set_flags(**self.fetch_args) \
            .return_reqs()
        
        return parameters
    
    @property
    def process(self):
        process: tuple = Executor() \
            .set_commands(**self.commands) \
            .return_proc()
        
        return process
    
    def add_command(self, flag: str, instructions: tuple):
        command = f'{flag.upper()}/{len(self.commands)}'
        self.commands[command] = instructions

    def engage(self, ent_data: tuple):

        # Data Fetching Process
        fetch_list = []
        for req in self.parameters.values():
            retrieved_data = req(ent_data)
            fetch_list.extend(retrieved_data)

        # Automatic Execution Process
        for step in self.process:
           step(fetch_list)
        return(fetch_list)



class Fetcher():
    def __init__(self) -> None:
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
        requirements = {}
        for flag in self.flags.items():
            requirements[flag[0]] = (self.parameter_flags[flag[0]](flag[1]))
        
        return requirements
    
    # Fetch Configuration Methods

    @staticmethod
    def fetch_attribute(info: tuple, *args: str) -> tuple:
        attr_dict: dict[str, int] = info[0]
        req_attrs = []
        for arg in args:
            gl.check_for_attribute(arg)

            req_attrs.append(attr_dict[arg.upper()])
        
        return tuple(req_attrs)
    
    @staticmethod
    def add_numbers(info: tuple, *args: int):
        for arg in args:
            gl.check_for_type(arg, int)

        return args

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
            'FETCH_STATS': lambda args: gl.data_slot_form(Fetcher.fetch_attribute, args),
            'ADD_NUMBERS': lambda args: gl.data_slot_form(Fetcher.add_numbers, args)
            }


class Executor():
    def __init__(self) -> None:
        self.commands: dict[str, tuple] = {}

    def set_commands(self, **kwargs: tuple):
        "Builder method for flags"

        commands: dict = {}

        for c, arg in enumerate(kwargs.items()):
            flag = arg[0].split('/')[0]
            if self.check_for_parameter_flag(flag.upper()):
                commands[arg[0]] = arg[1]
        
        self.commands = commands
        return self
    
    def return_proc(self) -> tuple:
        process = []
        for command in self.commands.items():
            flag = command[0].split('/')[0]
            process.append(self.parameter_flags[flag.upper()](command[1]))
        
        return tuple(process)

    @staticmethod
    def compose_variables(base_list: list, index_1: int, index_2: int, delete_second_element: bool = False) -> None:
        gl.check_for_type(base_list[index_1], int, message='list element indexed is the wrong type')
        gl.check_for_type(base_list[index_2], int, message='list element indexed is the wrong type')

        base_list[index_1] = base_list[index_1] * base_list[index_2]
        if delete_second_element:
            base_list[index_2] = None
    
    @staticmethod
    def roll_die(base_list: list, index_1: int) -> None:
        gl.check_for_type(base_list[index_1], Die, message='list element indexed is the wrong type')

        given_die: Die = base_list[index_1]

        base_list[index_1] = Die.roll(given_die)

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
            'ROLL_DIE': lambda args: gl.data_slot_form(Executor.roll_die, args),
            'COMPOSE': lambda args: gl.data_slot_form(Executor.compose_variables, args)
            }
    

if __name__ == '__main__':
    from Entity_Class import Entity
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