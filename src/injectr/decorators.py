import inspect
from functools import wraps
from typing import Callable, Optional, Type

from . import Registry, get_default_registry
from .loggers import logger
from .type_helpers import is_optional_type, get_type_that_optional_wraps


def inject_from(registry: Optional[Registry] = None, inject_missing_optional_as_none: bool = True) -> Callable:
    """Decorator that inspects the decorated function and injects instances from the provided registry if available."""

    def decorator(func: Callable) -> Callable:
        # Get decorated function's signature
        fn_signature = inspect.signature(func)

        @wraps(func)
        def wrapper(*args, **kwargs):
            # Get decorated function's bound_arguments
            bound_arguments = fn_signature.bind_partial(*args, **kwargs)
            bound_arguments.apply_defaults()

            # Skip params that already have an argument
            # Check which params misses arguments for us to look up in the registry;
            for param_name, param_val in fn_signature.parameters.items():
                is_optional_param: bool = is_optional_type(param_type=param_val.annotation)
                if param_name in bound_arguments.arguments:
                    has_value: bool = param_name in bound_arguments.arguments and bound_arguments.arguments[param_name] is not None
                    value_is_none = bound_arguments.arguments[param_name] is None
                    if has_value or (is_optional_param and value_is_none):
                        print(f"Skipping injection for '{param_name}' - already provided or optional with default None.")
                        continue


                # Attempt to retrieve from registry
                type_to_resolve:Type = get_type_that_optional_wraps(param_val.annotation)

                found_service = None
                logger.debug(f"Resolving parameter '{param_name}':{param_val.annotation} (type={type_to_resolve})")
                try:
                    found_service = registry.get(type_to_resolve, None)
                    logger.debug(f"found service: {found_service}")
                except Exception as e:
                    caller_provided_value:bool = param_name in bound_arguments.arguments
                    if not caller_provided_value and not is_optional_param:
                        raise ValueError(f"Cannot inject value for required parameter '{param_name}'. Error: {e}")
                    # eigher value for param is provided by user or param is optional; keep found_service=None


                # Actually inject a value, albeit None or the found service
                if found_service is not None:
                    logger.debug(f"Injecting resolved value for the parameter '{param_name}'")
                    bound_arguments.arguments[param_name] = found_service
                elif inject_missing_optional_as_none and is_optional_param:
                    # inject None for optional values if it can't be resolved
                    logger.debug(f"Injecting NONE for the optional parameter '{param_name}'")
                    bound_arguments.arguments[param_name] = None

            return func(*bound_arguments.args, **bound_arguments.kwargs)

        return wrapper

    return decorator


def inject(inject_missing_optional_as_none: bool = True) -> Callable:
    """Decorator that inspects the decorated function and injects instances from the provided registry if available."""

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            target_registry = get_default_registry()
            if target_registry is None:
                raise ValueError("No registries configured")

            inject_func = inject_from(
                registry=target_registry,
                inject_missing_optional_as_none=inject_missing_optional_as_none
            )(func)
            return inject_func(*args, **kwargs)

        return wrapper

    return decorator
