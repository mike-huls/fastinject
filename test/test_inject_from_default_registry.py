import logging
import unittest
from typing import NewType, Optional

import pytest

from src.injectr import inject_from, Registry, set_default_registry, get_default_registry
from src.injectr.decorators import inject
from test.objects_for_testing import services
from test.objects_for_testing.modules import ModuleDatabaseLogging, ModuleTimestamper


def test_inject_from_default_registry():
    """Test example"""
    # 1. Create registry
    registy = Registry(service_configs=[ModuleDatabaseLogging])
    assert get_default_registry() is not None

    @inject()
    def getlogger(logger: logging.Logger) -> None:
        print("in logger, logger = ", logger)
        assert logger is not None

    getlogger()


def test_inject_raises_if_module_not_registered_from_default_registry_double():
    """Test example"""
    # 1. Create registry
    registy = Registry(
        service_configs=[
            ModuleDatabaseLogging,
        ]
    )  # ModuleTimestamper])
    assert get_default_registry() is not None

    @inject()
    def getlogger(ts: services.TimeStamp, logger: logging.Logger) -> None: ...

    with pytest.raises(TypeError):
        getlogger()


def test_injects_none_on_missing_service():
    """Test example"""
    # 1. Create registry
    registy = Registry(
        service_configs=[
            ModuleDatabaseLogging,
        ]
    )  # ModuleTimestamper])
    assert get_default_registry() is not None

    @inject()
    def getlogger(logger: logging.Logger, ts: Optional[services.TimeStamp] = None) -> None:
        assert logger is not None
        assert ts is None

    getlogger()


def test_imperative():
    reg = get_default_registry()


# def test_inject_raises_if_no_registry_set():
#     """Injector searches in each function decorated with @provider"""
#     # 1. Make sure there is no global registry
#     # set_default_registry(None)
#     # registy = Registry(modules=[ModuleDatabaseLogging])
#
#     @inject()
#     def getlogger(ts:services.TimeStamp, logger: Optional[logging.Logger] = None) -> None:
#         ...
#
#     with pytest.raises(ValueError):
#         getlogger()
