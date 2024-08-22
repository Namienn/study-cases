import Global_Config as gl

class Ability():
    def __init__(self, **kwargs: tuple) -> None:
        self.parameters: dict = Fetcher() \
            .set_flags(**kwargs) \
            .return_reqs()
    
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


if __name__ == '__main__':
    walking = Ability(FETCH_STATS=('Vit', 'Str'))
    print(walking.parameters['FETCH_STATS']({'VIT': 10, 'STR': 15}))