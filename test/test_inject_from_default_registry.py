import logging
from typing import Optional

import pytest

from src.fastinject import Registry, get_default_registry
from src.fastinject.decorators import inject
from test.objects_for_testing import services
from test.objects_for_testing.modules import ModuleDatabaseLogging


def test_inject_from_default_registry():
    """Test example"""
    # 1. Create registry
    registy = Registry(service_configs=[ModuleDatabaseLogging])
    assert registy is not None
    assert get_default_registry() is not None

    @inject()
    def getlogger(_logger: logging.Logger) -> None:
        print("in logger, logger = ", _logger)
        assert _logger is not None

    getlogger()


def test_inject_raises_if_module_not_registered_from_default_registry_double():
    """Test example"""
    # 1. Create registry
    registy = Registry(
        service_configs=[
            ModuleDatabaseLogging,
        ]
    )  # ModuleTimestamper])
    assert registy is not None
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
    assert registy is not None
    assert get_default_registry() is not None

    @inject()
    def getlogger(_logger: logging.Logger, ts: Optional[services.TimeStamp] = None) -> None:
        assert _logger is not None
        assert ts is None

    getlogger()


def test_imperative():
    reg = get_default_registry()
    assert reg is not None


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
