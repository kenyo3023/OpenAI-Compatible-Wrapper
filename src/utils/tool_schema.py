import inspect
from enum import Enum
from typing import Any, Callable, get_type_hints


class TypeMappingEnum(Enum):
    """
    Enum class that maps Python types to JSON schema types.

    Attributes:
        str (str): Maps to 'string'.
        int (str): Maps to 'integer'.
        float (str): Maps to 'number'.
        bool (str): Maps to 'boolean'.
        list (str): Maps to 'array'.
        dict (str): Maps to 'object'.
    """
    str = 'string'
    int = 'integer'
    float = 'number'
    bool = 'boolean'
    list = 'array'
    dict = 'object'


def function_to_tool_schema(func:Callable[..., Any]) -> dict:
    """
    Converts a Python function into a OpenAI tool calling schema representation.

    Args:
        func (Callable[..., Any]): The function to convert.

    Returns:
        dict: A dictionary representing the function as a OpenAI tool calling schema.
              Includes function name, description, parameter types, and default values.

    Example:
        Given a function `def add(a: int, b: int): return a + b`,
        the returned schema will look like:
        {
            "type": "function",
            "function": {
                "name": "add",
                "description": "No description provided.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "a": {"type": "integer"},
                        "b": {"type": "integer"}
                    },
                    "required": ["a", "b"]
                }
            }
        }
    """
    name = func.__name__
    description = func.__doc__.strip().split("\n")[0] if func.__doc__ else "No description provided."
    sig = inspect.signature(func)
    parameters = sig.parameters
    type_hints = get_type_hints(func)

    schema = {
        'type': 'function',
        'function': None,
    }

    func_schema = {
        "name": name,
        "description": description,
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
        }
    }

    for param_name, param in parameters.items():
        param_schema = {}

        param_type = type_hints.get(param_name, Any)#.__name__
        param_schema["type"] = getattr(
            TypeMappingEnum, param_type.__name__#, TypeMappingEnum.str.name
        ).value

        if func.__doc__ and f"{param_name} (" in func.__doc__:
            start = func.__doc__.find(f"{param_name} (")
            desc = func.__doc__[start:].split("):", 1)[-1].strip().split("\n")[0]
            param_schema["description"] = desc

        if param.default != inspect.Parameter.empty:
            param_schema["default"] = param.default
        else:
            func_schema["parameters"]["required"].append(param_name)

        func_schema["parameters"]["properties"][param_name] = param_schema

    schema['function'] = func_schema
    return schema


def tool_schema_decorator(func:Callable[..., Any]):
    """
    A decorator that adds OpenAI tool calling schema representation to the decorated function.

    Args:
        func (Callable[..., Any]): The function to decorate.

    Returns:
        Callable[..., Any]: The wrapped function with an additional `schema` attribute.
                            The `schema` contains the function's OpenAI tool calling schema representation.

    Example:
        @tool_schema_decorator
        def add(a: int, b: int) -> int:
            return a + b

        add.schema -> OpenAI tool calling schema representation of the `add` function.
    """
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    schema = function_to_tool_schema(func)

    wrapper.schema = schema
    return wrapper


def is_decorated(func):
    """
    Determines whether a given function is decorated or wrapped.

    Args:
        func (Callable[..., Any]): The function to check.

    Returns:
        bool: True if the function is decorated, otherwise False.

    Notes:
        This function checks whether the function is decorated by comparing
        its `__name__` and `__qualname__` attributes.
    """
    # if hasattr(func, '__wrapped__'):
    #     return True

    # if func.__closure__ is not None:
    #     return True

    if func.__name__ != func.__qualname__:
        return True

    return False


if __name__ == '__main__':

    import json

    def get_weather(location: str, unit: str = "C") -> dict:
        """
        Get the current weather information for a specific location.
        Args:
            location (str): The location for which to get the weather.
            unit (str): The unit of temperature ('C' for Celsius, 'F' for Fahrenheit).
        Returns:
            dict: Weather information including temperature and description.
        """
        return {"temperature": 22, "description": "Sunny"}

    print(f'Validate the effectiveness of \033[34mfunction\033[0m case:')
    print(json.dumps(function_to_tool_schema(get_weather), indent=4))
    print()

    @tool_schema_decorator
    def get_weather(location: str, unit: str = "C") -> dict:
        """
        Get the current weather information for a specific location.
        Args:
            location (str): The location for which to get the weather.
            unit (str): The unit of temperature ('C' for Celsius, 'F' for Fahrenheit).
        Returns:
            dict: Weather information including temperature and description.
        """
        return {"temperature": 22, "description": "Sunny"}

    print(f'Validate the effectiveness of \033[34mdecorator\033[0m case:')
    print(json.dumps(get_weather.schema, indent=4))
    print()