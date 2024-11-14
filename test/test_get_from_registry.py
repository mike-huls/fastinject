import logging
import time
from typing import Type, TypeVar

from injector import ScopeDecorator, Scope, Provider

from src.fastinject import (
    Registry,
)
from test.objects_for_testing import services
from test.objects_for_testing.service_configs import (
    SCLogging,
    SCDatabase,
    SCTimestamper,
    SCTimestamperWeirdImport,
)
from test.objects_for_testing.services import DatabaseConfig, TimeStamp


# @patch('src.fastinject.registry.__default_registry', new_callable=lambda: Registry())
def test_get_from_registry():
    """Test example"""
    registry = Registry(service_configs=[SCLogging])
    assert registry.get(logging.Logger) is not None
    assert registry.get(SCTimestamper) is None


# @patch('src.fastinject.registry.__default_registry', new_callable=lambda: Registry())
# def test_get_from_registry(reg:Registry):


def test_can_get_from_registry_folder_import():
    """The service is imported like folder.Classname in the Module"""
    registry = Registry(service_configs=[SCTimestamperWeirdImport])
    assert registry.get(services.TimeStamp) is not None
    assert registry.get(TimeStamp) is not None


def test_get_from_registry_autobind():
    """Even though ModuleTimestamp is not registered on the registry, when we auto_bind=True, injector will resolve the dependency.
    This is becauase it searches the type in all functions decorated with @provider"""
    # Create registry
    registry = Registry(service_configs=[SCDatabase], auto_bind=True)

    # Can find both modules even though
    assert registry.get(DatabaseConfig) is not None
    assert registry.get(TimeStamp) is not None

    # Assert that ts is a full TimeStamp with all methods etc.
    ts: TimeStamp = registry.get(TimeStamp)
    assert ts is not None  # should be found
    assert "time_passed" in dir(ts)  # has 'time_passed' function
    assert isinstance(ts.time_passed(), float)
    time.sleep(0.001)
    assert ts.time_passed() > 0.0

def test_returns_none_in_exception_getting_from_registry():
    T = TypeVar('T')

    class ErrorScope(Scope):
        """Scope that thows an error on get """

        def get(self, unused_key: Type[T], provider: Provider[T]) -> Provider[T]:
            print(1 /0)
            return provider
    error_scope = ScopeDecorator(ErrorScope)
    registry = Registry(service_configs=[SCTimestamper])
    assert registry.get(TimeStamp, scope=error_scope) is None


