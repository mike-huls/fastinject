import logging
import time
import unittest
from typing import List

import pytest

from src.injectr import (
    inject_from,
    Registry,
    set_default_registry,
)
from test.objects_for_testing import services
from test.objects_for_testing.modules import (
    ModuleDatabaseLogging,
    ModuleLogging,
    ModuleDatabase,
    ModuleTimestamper,
    ModuleTimestamperWeirdImport,
)
from test.objects_for_testing.services import MyDatabaseConfig, TimeStamp


def test_get_from_registry():
    """Test example"""
    registry = Registry(service_configs=[ModuleLogging])
    assert registry.get(logging.Logger) is not None
    assert registry.get(ModuleTimestamper) is None


def test_can_get_from_registry_folder_import():
    """The service is imported like folder.Classname in the Module"""
    registry = Registry(service_configs=[ModuleTimestamperWeirdImport])
    assert registry.get(services.TimeStamp) is not None
    assert registry.get(TimeStamp) is not None


def test_get_from_registry_autobind():
    """Even though ModuleTimestamp is not registered on the registry, when we auto_bind=True, injector will resolve the dependency.
    This is becauase it searches the type in all functions decorated with @provider"""
    # Create registry
    registry = Registry(service_configs=[ModuleDatabase], auto_bind=True)

    # Can find both modules even though
    assert registry.get(MyDatabaseConfig) is not None
    assert registry.get(TimeStamp) is not None

    # Assert that ts is a full TimeStamp with all methods etc.
    ts: TimeStamp = registry.get(TimeStamp)
    assert ts is not None  # should be found
    assert "time_passed" in dir(ts)  # has 'time_passed' function
    assert isinstance(ts.time_passed(), float)
    time.sleep(0.001)
    assert ts.time_passed() > 0.0
