import inspect, logging
import os
from functools import wraps
from typing import Callable, Optional, Union, get_origin, get_args

from .default_registry import Registry

_logger = logging.getLogger(name="injectr")
_logger.setLevel(level=logging.WARNING)
# "global" variable to allow us to set/get a default registry
#     the getter/setter hide this from the application

__default_registry: Optional[Registry] = None


def set_default_registry(registry: Registry):
    global __default_registry
    __default_registry = registry


def get_default_registry() -> Registry:
    return __default_registry


def _get_logger() -> logging.Logger:
    return logging.getLogger(__file__)


def _is_optional_type(param):
    # if "Optional" in str(param):
    #    pass
    origin = get_origin(param)
    if origin is Union:
        args = get_args(param)
        if type(None) in args:  # Check if NoneType is part of the Union
            non_none_args = [arg for arg in args if arg is not type(None)]
            if len(non_none_args) == 1:
                return True
    if origin is Optional:
        return True
    return False


def _get_actual_type(param):
    # if "Optional" in str(param):
    #    pass
    if get_origin(param) is Union:
        args = get_args(param)
        if type(None) in args:  # Check if NoneType is part of the Union
            non_none_args = [arg for arg in args if arg is not type(None)]
            if len(non_none_args) == 1:
                return non_none_args[0]
    if get_origin(param) is Optional:
        return param.__args__[0]
    return param


def inject_services(registry: Optional[Registry] = None, inject_missing_optional_as_none: bool = True) -> Callable:
    """Decorator that inspects the decorated function and injects instances from the provided registry if available."""

    # maybe we should do this later
    # if registry is None:
    #    registry = get_default_registry()
    def decorator(func: Callable) -> Callable:
        # Get decorated function's signature
        fn_signature = inspect.signature(func)

        @wraps(func)
        def wrapper(*args, **kwargs):
            target_registry = registry
            if target_registry is None:
                target_registry = get_default_registry()
            # Get decorated function's bound_arguments
            bound_arguments = fn_signature.bind_partial(*args, **kwargs)
            bound_arguments.apply_defaults()

            # Check which params miss arguments for us to look up in the registry
            for param_name, param_val in fn_signature.parameters.items():
                if param_name in bound_arguments.arguments:
                    # Skip if the argument is already provided
                    # For optional parameters still attempt to resovle them if the value is None
                    if not _is_optional_type(param_val.annotation) or bound_arguments.arguments[param_name] is not None:
                        _logger.debug(f" Skipping parameter {param_name} because it got a value ")
                        continue

                # Attempt to retrieve from registry
                type_to_resolve = _get_actual_type(param_val.annotation)
                from_registry = None
                _logger.debug(
                    f"Attempting to resolve parameter {param_name}:{param_val.annotation}. Type to resolve {type_to_resolve}"
                )
                try:
                    from_registry = target_registry.get(type_to_resolve, None)
                except:
                    if param_name not in bound_arguments.arguments and not _is_optional_type(param_val.annotation):
                        # no default value (None) was provided
                        # this could indicate a bug in the code so we log a warning
                        _logger.warning(
                            f"Failed to resolve/create instance of type {param_name}:{type_to_resolve}. Was this an optional type?"
                        )
                        # logger.exception(f"Failed to resolve/create instance of type {param_name}:{type_to_resolve}")
                        continue
                    from_registry = None

                if from_registry is not None:
                    _logger.debug(f"Injecting resolved value for the parameter {param_name}")
                    bound_arguments.arguments[param_name] = from_registry
                elif inject_missing_optional_as_none and _is_optional_type(param_val.annotation):
                    # inject None for optional values if it can't be resolved
                    _logger.debug(f"Injecting NONE for the optional parameter {param_name}")
                    bound_arguments.arguments[param_name] = None

            return func(*bound_arguments.args, **bound_arguments.kwargs)

        return wrapper

    return decorator
