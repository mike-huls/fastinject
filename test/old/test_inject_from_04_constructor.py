import logging
import unittest
from typing import NewType, Optional

from src.injectr import (
    inject_services as inject_from,
    set_default_registry,
    Registry,
    RegistryBuilder,
)
from test.objects_for_testing.registries import RegDatabaseLogging, RegDatabase

ConnectionString = NewType("ConnectionString", str)


class TestObject:
    @inject_from()
    def __init__(self, logger: Optional[logging.Logger]) -> None:
        self._logger = logger

    def get_logger(self) -> logging.Logger:
        return self._logger


def test_inject_from_works():
    """Test example"""
    # 1. Create registry
    registry_builder = RegistryBuilder.create()
    registry_builder.add_module(RegDatabase)
    registry: Registry = registry_builder.build()
    set_default_registry(registry)
    # @inject_from()
    instance = TestObject()
    # should be None
    assert instance.get_logger() is None
