import logging
from typing import List

import pytest

from src.injectr import (
    inject_from,
    Registry,
)
from test.objects_for_testing.modules import ModuleLogging, ModuleDatabase
from test.objects_for_testing.services import MyDatabaseConfig


def test_can_inject_from():
    # 1. Create registry
    registry = Registry(modules=[ModuleLogging, ModuleDatabase])

    # 2. Decorate functions with registry to inject from
    @inject_from(registry=registry)
    def inject_logger_in_fn(logger: logging.Logger):
        assert logger is not None

    @inject_from(registry=registry)
    def inject_dbconfig_in_fn(dbcon: MyDatabaseConfig):
        assert dbcon is not None
        assert dbcon.connection_string == "file:memdb1?mode=memory&cache=shared3"

    @inject_from(registry=registry)
    def inject_both(dbcon: MyDatabaseConfig, logger: logging.Logger):
        assert dbcon is not None
        assert dbcon.connection_string == "file:memdb1?mode=memory&cache=shared3"
        assert logger is not None

    # 3. Call decorated functions
    inject_logger_in_fn()
    inject_dbconfig_in_fn()
    inject_both()

def test_raises_typeerror_on_nonregistered_type():
    """ Cannot get type form container that isn't registered; throws """

    # 1. Create registry
    registry = Registry(modules=[ModuleLogging, ModuleDatabase])

    @inject_from(registry=registry)
    def inject_non_existent(logger: List):
        assert logger is None

    with pytest.raises(TypeError):
        inject_non_existent()

def test_can_inject_in_class():
    # 1. Create registry
    registry = Registry(modules=[ModuleLogging, ModuleDatabase])

    # 2. Decorate class with registry to inject from
    class MyClass:
        @inject_from(registry=registry)
        def __init__(self, logger: logging.Logger):
            self.logger = logger
            assert logger is not None

    # 3. Create instance and call decorated function
    my_class = MyClass()


# if __name__ == '__main__':
#     unittest.main()
