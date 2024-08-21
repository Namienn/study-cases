import Global_Config as gl

class Ability():
    def __init__(self) -> None:
        self.parameters: Fetcher = Fetcher()


class Fetcher():
    def __init__(self) -> None:
        self.flags: tuple = ()
    
    def set_flags(self, *args: str):
        "Builder method for flags"

        for arg in args:
            gl.check_for_parameter_flag(arg)
        
        self.flags = args
        return self