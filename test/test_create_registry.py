import logging

from src.fastinject import Registry
from test.objects_for_testing import services
from test.objects_for_testing.service_configs import SCLogging, SCDatabase
from test.objects_for_testing.services import DatabaseConfig


def test_create_registry_init_works():
    """Test example"""
    registry_builder = Registry()
    assert len(registry_builder._service_configs) == 0
    registry_builder.add_service_config(SCLogging)
    assert len(registry_builder._service_configs) == 1
    assert registry_builder.get(logging.Logger) is not None
    assert len(registry_builder._service_configs) == 1
    assert str(registry_builder) == f"<Registry (1 service configs, 0 services)>"
    assert repr(registry_builder) == f"<Registry (1 service configs, 0 services)>"


def test_create_registry_pass_modules_in_init_works():
    """Test example"""
    registry_builder = Registry(service_configs=[SCLogging, SCDatabase])
    assert len(registry_builder._service_configs) == 2
    assert registry_builder.get(logging.Logger) is not None


def test_create_registry_init_then_add_works():
    """Test example"""
    registry_builder = Registry(service_configs=[SCDatabase])
    assert len(registry_builder._service_configs) == 1
    registry_builder.add_service_config(service_config=SCLogging)
    assert len(registry_builder._service_configs) == 2
    assert registry_builder.get(logging.Logger) is not None
    assert registry_builder.get(DatabaseConfig) is not None


def test_create_registry_add_service_works():
    registy = Registry()
    registy.add_service(service=services.TimeStamp)
    assert registy.get(interface=services.TimeStamp) is not None


def test_create_registry_with_services():
    registy = Registry(services=[services.TimeStamp])
    assert registy.get(interface=services.TimeStamp) is not None
