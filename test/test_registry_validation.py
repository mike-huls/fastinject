import pytest

from src.fastinject import Registry, set_default_registry
from test.objects_for_testing import services, service_configs


def test_can_validate_correct_services_and_configs():
    """Test example"""
    # 1. Create registry
    set_default_registry(registry=None)
    registy = Registry(services=[services.TimeStamp], service_configs=[service_configs.SCDatabase])
    assert registy is not None
    # assert get_default_registry() is not None

    # Below does not throw exception if all services can be instantiated
    registy.validate()


def test_validate_raises_on_invalid_service_config():
    """Test example"""
    # 1. Create registry
    set_default_registry(registry=None)
    registy = Registry(
        services=[services.TimeStamp], service_configs=[service_configs.SCDatabaseInitFails], auto_validate=False
    )
    assert registy is not None
    # assert get_default_registry() is not None

    # DatabaseConnection, DatabaseConfig, TimeStamp
    with pytest.raises(ValueError):
        registy.validate()


def test_validate_raises_on_invalid_service():
    """Test example"""
    # 1. Create registry
    set_default_registry(registry=None)
    registy = Registry(
        services=[services.ErrorsOnInit], service_configs=[service_configs.SCDatabase], auto_validate=False
    )
    assert registy is not None
    # assert get_default_registry() is not None

    # DatabaseConnection, DatabaseConfig, TimeStamp
    with pytest.raises(ValueError):
        registy.validate()
