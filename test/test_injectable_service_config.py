import logging
from typing import List, Optional

import pytest
from injector import singleton, provider

from src.fastinject import Registry, inject, injectable, ServiceConfig
from test.objects_for_testing.service_configs_injectable import ModuleLogging, ModuleDatabase
from test.objects_for_testing.registries import DummyRegistry
from test.objects_for_testing.services import DatabaseConfig
from test.objects_for_testing.services_injectable import NotInjectedService, TimeStamp


class NonRegisteredClass:
    pass


@pytest.fixture(scope="function")
def test_can_inject_with_autobind():
    # 1. Decorate functions to inject from (default) registry. Registry is created with @injectable on service
    @inject()
    def inject_logger_in_fn(_logger: logging.Logger):
        assert _logger is not None

    # 3. Call decorated functions
    inject_logger_in_fn()


@pytest.fixture(scope="function")
def test_sc_catch_error_in_getting_service_from_registry():
    # 1. Decorate functions to inject from (default) registry. Registry is created with @injectable on service
    @inject()
    def injected_fn(noop: NotInjectedService, ts: TimeStamp):
        pass

    # 2. Call decorated functions
    with pytest.raises(TypeError):
        # TimeStamp is correctly decorated with @injectable on service, NotInjectedService is not
        injected_fn()


def test_inject_none_if_error_in_getting_optional_service_from_registry():
    # 1. Create registry
    registry = DummyRegistry()
    assert registry is not None

    # 2. Decorate functions with registry to inject from
    @inject()
    def injected_fn(val: Optional[NonRegisteredClass] = None):
        assert val is None

    # 3. Call decorated functions
    injected_fn()


@pytest.fixture(scope="function")
def test_raises_on_injecting_unregisterd_required_object():
    # 2. Decorate functions with registry to inject from
    @inject()
    def inject_logger_in_fn(my_inst: NonRegisteredClass): ...

    # Should fail because it cannot inject requried SomeClass type
    with pytest.raises(TypeError):
        inject_logger_in_fn()


def test_returns_none_on_injecting_unregisterd_optional_object():
    # 2. Decorate functions with registry to inject from
    @inject()
    def inject_logger_in_fn(my_inst: Optional[NonRegisteredClass]):
        assert my_inst is None

    # Should fail because it cannot inject requried SomeClass type
    inject_logger_in_fn()


def test_raises_on_injecting_unregisterd_optional_object_when_not_inject_none():
    # 1. Decorate functions with registry to inject from
    @inject(inject_missing_optional_as_none=False)
    def inject_logger_in_fn(my_inst: Optional[NonRegisteredClass]):
        assert my_inst is None

    # Should fail because it cannot inject requried SomeClass type
    with pytest.raises(TypeError):
        inject_logger_in_fn()


def test_can_inject_from_with_optional_dependency():
    # 1. Create registry
    registry = Registry(service_configs=[ModuleLogging, ModuleDatabase])
    assert registry is not None

    # 2. Decorate functions with registry to inject from
    @inject()
    def inject_logger_in_fn(_logger: Optional[logging.Logger]):
        assert _logger is not None

    @inject()
    def inject_dbconfig_in_fn(dbcon: DatabaseConfig):
        assert dbcon is not None
        assert dbcon.connection_string == "file:memdb1?mode=memory&cache=shared3"

    @inject()
    def inject_both(dbcon: DatabaseConfig, _logger: logging.Logger):
        assert dbcon is not None
        assert dbcon.connection_string == "file:memdb1?mode=memory&cache=shared3"
        assert _logger is not None

    # 3. Call decorated functions
    inject_logger_in_fn()
    inject_dbconfig_in_fn()
    inject_both()


@pytest.fixture(scope="function")
def test_can_inject_from_with_additional_args():
    @inject()
    def inject_logger_in_fn(_logger: logging.Logger, a: int, b: int = 1, c: Optional[int] = None):
        assert _logger is not None
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


@pytest.fixture(scope="function")
def test_raises_typeerror_on_nonregistered_type_with_injectable():
    """Cannot get type form container that isn't registered; throws"""

    @inject()
    def inject_non_existent(_logger: List):
        assert _logger is None

    with pytest.raises(TypeError):
        inject_non_existent()


def test_can_inject_in_class():
    # 2. Decorate class with registry to inject from
    class MyClass:
        @inject()
        def __init__(self, _logger: logging.Logger):
            self.logger = _logger
            assert _logger is not None

    # 3. Create instance and call decorated function
    my_class = MyClass()
    assert my_class is not None


def test_raises_when_decorating_wrongtype_class_with_injectables():
    @injectable()
    class ModuleDatabase(ServiceConfig):
        # todo test wheteher only some functions within a class can be providers
        @provider
        def provide_config(self) -> DatabaseConfig:
            return DatabaseConfig(connection_string="file:memdb1?mode=memory&cache=shared3")
