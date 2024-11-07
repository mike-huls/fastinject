import logging
import unittest
from typing import NewType, Optional

from src.injectr import inject_from, RegistryDEPRECATED, Registry
from test.objects_for_testing.modules import ModuleDatabaseLogging

ConnectionString = NewType("ConnectionString", str)


class TestObject:
    @inject_from()
    def __init__(self, logger: Optional[logging.Logger] = None) -> None:
        self._logger = logger

    def get_logger(self) -> logging.Logger:
        return self._logger

    @inject_from()
    def get_logger2(self, logger: logging.Logger) -> logging.Logger:
        return logger


def test_inject_from_works():
    """Test example"""
    # 1. Create registry
    registry_builder = Registry()
    registry_builder.add_module(ModuleDatabaseLogging)
    registry: RegistryDEPRECATED = registry_builder.build()
    # @inject_from()
    instance = TestObject()
    assert instance.get_logger() is not None
    assert instance.get_logger2() is not None
