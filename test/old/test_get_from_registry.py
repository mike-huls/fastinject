import logging
import time
import unittest
from typing import List

import pytest

from src.injectr import (
    inject_services as inject_from,
    Registry,
    set_default_registry,
)
from test.objects_for_testing.modules import ModuleDatabaseLogging, ModuleLogging, ModuleDatabase, ModuleTimestamper, ModuleTimestamperWeirdImport
from test.objects_for_testing.services import MyDatabaseConfig, TimeStamp


def test_get_from_registry():
    """Test example"""
    registry = Registry(modules=[ModuleLogging])
    assert registry.get(logging.Logger) is not None
    assert registry.get(ModuleTimestamper) is None

def test_can_get_from_registry_folder_import():
    """The service is imported like folder.Classname in the Module """
    registry = Registry(modules=[ModuleTimestamperWeirdImport])
    assert registry.get(ModuleTimestamperWeirdImport) is not  None

def test_get_from_registry_autobind():
    """ Even though ModuleTimestamp is not registered on the registry, when we auto_bind=True, injector will resolve the dependency.
    This is becauase it searches the type in all functions decorated with @provider """
    # Create registry
    registry = Registry(modules=[ModuleDatabase], auto_bind=True)

    # Can find both modules even though
    assert registry.get(MyDatabaseConfig) is not None
    assert registry.get(TimeStamp) is not None

    # Assert that ts is a full TimeStamp with all methods etc.
    ts:TimeStamp = registry.get(TimeStamp)
    assert ts is not None               # should be found
    assert 'time_passed' in dir(ts)     # has 'time_passed' function
    assert isinstance(ts.time_passed(), float)
    time.sleep(0.001)
    assert ts.time_passed() > 0.0

# ------------------------------------------------------------------------------------------------------
def test_inject_from_works():
    """Test example"""
    # 1. Create registry
    registry = Registry(modules=[ModuleLogging, ModuleDatabase])
    set_default_registry(None)

    @inject_from(registry=registry)
    def inject_logger_in_fn(logger: logging.Logger):
        assert logger is not None

    inject_logger_in_fn()

    @inject_from(registry=registry)
    def inject_dbconfig_in_fn(dbcon: MyDatabaseConfig):
        assert dbcon is not None
        assert dbcon.connection_string == "file:memdb1?mode=memory&cache=shared3"

    inject_dbconfig_in_fn()

    @inject_from(registry=registry)
    def inject_both(dbcon: MyDatabaseConfig, logger: logging.Logger):
        assert dbcon is not None
        assert dbcon.connection_string == "file:memdb1?mode=memory&cache=shared3"
        assert logger is not None

    inject_both()

    # Cannot get type form container that isn't registered; throws
    @inject_from(registry=registry)
    def inject_non_existent(logger: List):
        assert logger is None

    with pytest.raises(Exception):
        inject_non_existent()


# if __name__ == '__main__':
#     unittest.main()
