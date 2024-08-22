import Global_Config as gl

class Ability():
    def __init__(self, **kwargs: tuple) -> None:
        self.parameters: dict = Fetcher() \
            .set_flags(**kwargs) \
            .return_reqs()
        
        self.process: None = Executor() \
            .set_flags(**kwargs) \
            .return_proc()
    
    def engage(self, ent_data: tuple):
        pass


class Fetcher():
    def __init__(self) -> None:
        self.flags: dict[str, tuple]
    
    def set_flags(self, **kwargs: tuple):
        "Builder method for flags"

        for arg in kwargs.items():
            self.check_for_parameter_flag(arg[0])
        
        self.flags = kwargs
        return self
    
    def return_reqs(self) -> dict:
        requirements = {}
        for flag in self.flags.items():
            requirements[flag[0]] = (self.parameter_flags[flag[0]](flag[1]))
        
        return requirements
    
    # Fetch Configuration Methods

    @staticmethod
    def fetch_attribute(attr_dict: dict[str, int], *args: str) -> tuple:
        req_attrs = []
        for arg in args:
            gl.check_for_attribute(arg)

            req_attrs.append(attr_dict[arg.upper()])
        
        return tuple(req_attrs)

    # Fetch Parameter Flags

    @classmethod
    def check_for_parameter_flag(cls, element: str, message: str = 'Parameter is not a valid flag') -> None:
        "Function to confirm if a given string qualifies as a parameter flag"

        gl.check_in_config(element, cls.parameter_flags.keys(), message)    

    parameter_flags = {
            'FETCH_STATS': lambda args: gl.data_slot_form(Fetcher.fetch_attribute, args)
            }


class Executor():
    def __init__(self) -> None:
        self.flags: dict[str, tuple]

    def set_flags(self, **kwargs: tuple):
        "Builder method for flags"

        for arg in kwargs.items():
            self.check_for_parameter_flag(arg[0])
        
        self.flags = kwargs
        return self
    
    def return_proc(self) -> None:
        pass

    @staticmethod
    def compose_variables(base_list: list, in_1: int, in_2: int, delete_second_element: bool = False):
        gl.check_for_type(base_list[in_1], int, message='list element indexed is the wrong type')
        gl.check_for_type(base_list[in_2], int, message='list element indexed is the wrong type')

        base_list[in_1] = base_list[in_1] * base_list[in_2]
        if delete_second_element:
            base_list[in_2] = None

    # Execute Parameter Flags
    
    @classmethod
    def check_for_parameter_flag(cls, element: str, message: str = 'Parameter is not a valid flag') -> None:
        "Function to confirm if a given string qualifies as a parameter flag"

        gl.check_in_config(element, cls.parameter_flags.keys(), message)    

    parameter_flags = {
            'FETCH_STATS': None
            }
    

if __name__ == '__main__':
    walking = Ability(FETCH_STATS=('Vit', 'Str'))
    print(walking.parameters['FETCH_STATS']({'VIT': 10, 'STR': 15}))

    test_list = ['5', 2]
    Executor.compose_variables(test_list, 0, 1)
    print(test_list)
    Executor.compose_variables(test_list, 0, 1)
    print(test_list)
    Executor.compose_variables(test_list, 0, 1)
    print(test_list)

    # Where i've stopped: Setting how parameters will be given to methods

    # What i must do next:
    # - Experiment and define how different steps chain with each other
    # - Figure out how to export the whole process from the Executor class
    # - Ensure the data structure reliability of the Fetcher output