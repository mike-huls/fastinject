import logging
import unittest
from typing import List

import pytest

from src.injectr import (
    inject_services as inject_from,
    RegistryDEPRECATED,
    Registry,
    set_default_registry,
)
from test.objects_for_testing.registries import RegDatabaseLogging, RegLogging, RegDatabase
from test.objects_for_testing.services import MyDatabaseConfig


def test_get_from_registry_by_type():
    """Test example"""
    registry = Registry(modules=[RegLogging, RegDatabase])
    assert registry.get(logging.Logger) is not None
    assert registry.get(RegDatabase) is not None

def test_get_from_registry_by_type():
    """Test example"""
    registry = Registry(modules=[RegLogging])
    assert registry.get(logging.Logger) is not None
    print("NNNNNNNNNNNNNNNn")
    print(registry.get(RegDatabase))
    print(registry._modules)
    # assert registry.get(RegDatabase) is None


def test_inject_from_works():
    """Test example"""
    # 1. Create registry
    registry = Registry.create()
    registry.add_module(RegDatabaseLogging)
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
