from . import Global_Config as gl

# This file contains the functions utilized by the
# Fetcher class owned by an Ability object.
#
# The functions are referenced through the lambda
# method by the flags, allowing for externalization
# of the utilized functions.

def fetch_attribute(info: tuple, *args: str) -> tuple:
    "Function for fetching the pure attribute value from an entity"

    attr_dict: dict[str, int] = info[0]
    req_attrs = []
    for arg in args:
        gl.check_for_attribute(arg)

        req_attrs.append(attr_dict[arg.upper()])
    
    return tuple(req_attrs)

@staticmethod
def add_numbers(info: tuple, *args: int):
    "Function for adding predefined numbers to the value list"

    for arg in args:
        gl.check_for_type(arg, int)

    return args