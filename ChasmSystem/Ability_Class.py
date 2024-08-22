import Global_Config as gl

class Ability():
    def __init__(self, *args) -> None:
        self.parameters: tuple = Fetcher() \
            .set_flags(*args) \
            .return_reqs()
    
    def engage(self, ent_data: tuple):
        pass


class Fetcher():
    def __init__(self) -> None:
        self.flags: tuple[str, ...]
    
    def set_flags(self, *args: str):
        "Builder method for flags"

        for arg in args:
            self.check_for_parameter_flag(arg)
        
        self.flags = args
        return self
    
    def return_reqs(self) -> tuple:
        requirements = []
        for flag in self.flags:
            requirements.append(self.parameter_flags[flag.upper()])
        
        return tuple(requirements)
    
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
            'FETCH_STATS': lambda data, *args: Fetcher.fetch_attribute(data, *args)
            }


if __name__ == '__main__':
    walking = Ability('FETCH_STATS')
    print(walking.parameters[0]({'VIT': 10}, 'Vit'))