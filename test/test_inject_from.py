import logging
import time
from typing import List, Optional

import pytest

from src.fastinject import (
    inject_from,
    Registry,
    logger,
)
from test.objects_for_testing import services
from test.objects_for_testing.modules import ModuleLogging, ModuleDatabase, ModuleNestedDependenciesSimple
from test.objects_for_testing.registries import DummyRegistry
from test.objects_for_testing.services import MyDatabaseConfig, TimeStampLogger


class NonRegisteredClass:
    pass


def test_can_inject_from():
    # 1. Create registry
    registry = Registry(service_configs=[ModuleLogging, ModuleDatabase])

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


def test_catch_error_in_getting_service_from_registry():
    # 1. Create registry
    registry = DummyRegistry()

    # 2. Decorate functions with registry to inject from
    @inject_from(registry=registry)
    def injected_fn(dbcon: MyDatabaseConfig, logger: logging.Logger):
        assert dbcon is not None
        assert dbcon.connection_string == "file:memdb1?mode=memory&cache=shared3"
        assert logger is not None

    # 3. Call decorated functions
    with pytest.raises(ValueError):
        injected_fn()


def test_inject_none_if_error_in_getting_optional_service_from_registry():
    # 1. Create registry
    registry = DummyRegistry()

    # 2. Decorate functions with registry to inject from
    @inject_from(registry=registry)
    def injected_fn(dbcon: Optional[MyDatabaseConfig] = None):
        assert dbcon is None

    # 3. Call decorated functions
    injected_fn()


def test_raises_on_injecting_unregisterd_required_object():
    # 1. Create registry
    registry = Registry(service_configs=[ModuleLogging, ModuleDatabase])

    # 2. Decorate functions with registry to inject from
    @inject_from(registry=registry)
    def inject_logger_in_fn(my_inst: NonRegisteredClass): ...

    # Should fail because it cannot inject requried SomeClass type
    with pytest.raises(TypeError):
        inject_logger_in_fn()


def test_returns_none_on_injecting_unregisterd_optional_object():
    # 1. Create registry
    registry = Registry(service_configs=[ModuleLogging, ModuleDatabase])

    # 2. Decorate functions with registry to inject from
    @inject_from(registry=registry)
    def inject_logger_in_fn(my_inst: Optional[NonRegisteredClass]):
        assert my_inst is None

    # Should fail because it cannot inject requried SomeClass type
    inject_logger_in_fn()


def test_raises_on_injecting_unregisterd_optional_object_when_not_inject_none():
    # 1. Create registry
    registry = Registry(service_configs=[ModuleLogging, ModuleDatabase])

    # 2. Decorate functions with registry to inject from
    @inject_from(registry=registry, inject_missing_optional_as_none=False)
    def inject_logger_in_fn(my_inst: Optional[NonRegisteredClass]):
        assert my_inst is None

    # Should fail because it cannot inject requried SomeClass type
    with pytest.raises(TypeError):
        inject_logger_in_fn()


def test_can_inject_from_nested_dependencies():
    # 1. Create registry
    registry = Registry(service_configs=[ModuleNestedDependenciesSimple])

    @inject_from(registry=registry)
    def inject_logger_in_fn(ts: services.TimeStamp, tslogger: TimeStampLogger):
        assert ts is not None
        assert tslogger is not None
        print(tslogger.timestamp.init_time)

    # 3. Call decorated functions
    inject_logger_in_fn()
    time.sleep(0.1)
    inject_logger_in_fn()
    time.sleep(0.2)


def test_can_inject_from_with_optional_dependency():
    # 1. Create registry
    registry = Registry(service_configs=[ModuleLogging, ModuleDatabase])

    # 2. Decorate functions with registry to inject from
    @inject_from(registry=registry)
    def inject_logger_in_fn(logger: Optional[logging.Logger]):
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


def test_can_inject_from_with_additional_args():
    # 1. Create registry
    registry = Registry(service_configs=[ModuleLogging, ModuleDatabase])

    # 2. Decorate functions with registry to inject from
    @inject_from(registry=registry)
    def inject_logger_in_fn(logger: logging.Logger, a: int, b: int = 1, c: Optional[int] = None):
        assert logger is not None
        assert isinstance(a, int)
        assert isinstance(b, int)
        assert isinstance(c, int) or c is None

    # 3. Call decorated functions
    inject_logger_in_fn(a=5, b=4, c=4)
    inject_logger_in_fn(a=5, b=4, c=None)
    inject_logger_in_fn(a=5)
    with pytest.raises(TypeError):
        # a is required; shoudle be provided
        inject_logger_in_fn()
        inject_logger_in_fn(b=5)
        inject_logger_in_fn(c=5)


def test_raises_typeerror_on_nonregistered_type():
    """Cannot get type form container that isn't registered; throws"""

    # 1. Create registry
    registry = Registry(service_configs=[ModuleLogging, ModuleDatabase])

    @inject_from(registry=registry)
    def inject_non_existent(logger: List):
        assert logger is None

    with pytest.raises(TypeError):
        inject_non_existent()


def test_can_inject_in_class():
    # 1. Create registry
    registry = Registry(service_configs=[ModuleLogging, ModuleDatabase])

    # 2. Decorate class with registry to inject from
    class MyClass:
        @inject_from(registry=registry)
        def __init__(self, logger: logging.Logger):
            self.logger = logger
            assert logger is not None

    # 3. Create instance and call decorated function
    my_class = MyClass()
