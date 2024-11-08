import logging

from src.fastinject import Registry
from test.objects_for_testing import services
from test.objects_for_testing.modules import ModuleLogging, ModuleDatabase
from test.objects_for_testing.services import MyDatabaseConfig


def test_create_registry_init_works():
    """Test example"""
    registry_builder = Registry()
    assert len(registry_builder._modules) == 0
    registry_builder.add_service_config(ModuleLogging)
    assert len(registry_builder._modules) == 1
    assert registry_builder.get(logging.Logger) is not None
    assert len(registry_builder._modules) == 1


def test_create_registry_pass_modules_in_init_works():
    """Test example"""
    registry_builder = Registry(service_configs=[ModuleLogging, ModuleDatabase])
    assert len(registry_builder._modules) == 2
    assert registry_builder.get(logging.Logger) is not None


def test_create_registry_init_then_add_works():
    """Test example"""
    registry_builder = Registry(service_configs=[ModuleDatabase])
    assert len(registry_builder._modules) == 1
    registry_builder.add_service_config(service_config=ModuleLogging)
    assert len(registry_builder._modules) == 2
    assert registry_builder.get(logging.Logger) is not None
    assert registry_builder.get(MyDatabaseConfig) is not None


def test_create_registry_add_service_works():
    registy = Registry()
    registy.add_service(service=services.TimeStamp)
    assert registy.get(interface=services.TimeStamp) is not None


def test_create_registry_with_services():
    registy = Registry(services=[services.TimeStamp])
    assert registy.get(interface=services.TimeStamp) is not None
