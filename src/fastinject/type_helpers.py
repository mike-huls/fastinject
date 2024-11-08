from typing import get_origin, Union, get_args, Optional, Type


def is_optional_type(param_type: Type) -> bool:
    """Check if a type is Optional (Union with None).
    Type is Optional when it has a default value
    """
    origin = get_origin(param_type)
    return origin is Union and type(None) in get_args(param_type)


def get_type_that_optional_wraps(param_type: Type) -> Type:
    """Extract the actual type from an Optional type."""
    if is_optional_type(param_type):
        return next(arg for arg in get_args(param_type) if arg is not type(None))
    return param_type
