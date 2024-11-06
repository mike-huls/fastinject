import logging

from src.injectr import Registry
from test.objects_for_testing.registries import RegLogging, RegDatabase
from test.objects_for_testing.services import MyDatabaseConfig


def test_create_registry_classmethod_works():
    """Test example"""
    registry_builder = Registry.create()
    assert len(registry_builder._modules) == 0
    registry_builder.add_module(RegLogging)
    assert len(registry_builder._modules) == 1
    assert registry_builder.get(logging.Logger) is not None
    assert len(registry_builder._modules) == 1

def test_create_registry_init_works():
    """Test example"""
    registry_builder = Registry()
    assert len(registry_builder._modules) == 0
    registry_builder.add_module(RegLogging)
    assert len(registry_builder._modules) == 1
    assert registry_builder.get(logging.Logger) is not None
    assert len(registry_builder._modules) == 1


def test_create_registry_pass_modules_in_init_works():
    """Test example"""
    registry_builder = Registry(modules=[RegLogging, RegDatabase])
    assert len(registry_builder._modules) == 2
    assert registry_builder.get(logging.Logger) is not None

def test_create_registry_init_then_add_works():
    """Test example"""
    registry_builder = Registry(modules=[RegDatabase])
    assert len(registry_builder._modules) == 1
    registry_builder.add_module(module=RegLogging)
    assert len(registry_builder._modules) == 2
    assert registry_builder.get(logging.Logger) is not None
    assert registry_builder.get(MyDatabaseConfig) is not None