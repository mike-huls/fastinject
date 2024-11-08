import datetime
import inspect
import logging
import time
import uuid
from functools import wraps
from typing import Callable, Optional

from src.injectr import Registry, Module, singleton, provider, inject_from, inject, logger, get_default_registry
from src.injectr.type_helpers import is_optional_type, get_type_that_optional_wraps


def injectable(original_class):
    orig_init = original_class.__init__
    # Make copy of original __init__, so we can call it without recursion
    print("11111111")

    def __init__(self, *args, **kws):
        self.my_id = uuid.uuid4()
        orig_init(self, *args, **kws) # Call the original __init__

    def configure_for_testing(binder):
        """ Puts a service in a registry without the decorators """
        binder.bind(original_class, to=original_class(), scope=singleton)

    # Create empty registry; no modules added todo add registry to decorator
    print("default", get_default_registry())
    registry = get_default_registry() or Registry()
    print('in_register', registry)
    registry.add_setup_function(configure_for_testing)
    logger.debug("added setup")

    #

    original_class.__init__ = __init__ # Set the class' __init__ to the new one
    return original_class


class TimeStamp:
    init_time: float
    def __init__(self) -> None:
        self.init_time = time.time()
    def to_string(self) -> str:
        return datetime.datetime.fromtimestamp(self.init_time).strftime("%Y-%m-%d %H:%M:%S")

@injectable
class IdGenerator:
    the_id: str
    def __init__(self) -> None:
        self.the_id = str(uuid.uuid4())

class ServiceConfig(Module):
    @singleton
    @provider
    def provide_timestamper(self) -> TimeStamp:
        return TimeStamp()

    @singleton
    @provider
    def provide_logger(self) -> logging.Logger:
        return logging.getLogger("LoggerName")


print("JJJJ", get_default_registry())
registry = get_default_registry()
registry.add_module(module=ServiceConfig)
# registry = Registry(modules=[ServiceConfig])



@inject()
def function_with_injection(_logger: logging.Logger, ts: TimeStamp, idgen:IdGenerator):
    _logger.setLevel(level=logging.DEBUG)
    _logger.warning(f"Hello from within the function! Time: {ts.to_string()}")
    _logger.warning(f"injected id: {ts.to_string()}")
    _logger.warning(f"idgen: {idgen}")
    _logger.warning(f"idgen: {idgen.the_id}")

if __name__ == "__main__":
    logger.setLevel(level=logging.DEBUG)

    function_with_injection()