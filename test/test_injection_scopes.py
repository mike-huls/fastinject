import pytest

from src.fastinject import Registry
from test.objects_for_testing.service_configs import SCDatabase, SCTimestamper
from test.objects_for_testing.services import DatabaseConfig, TimeStamp


def test_singleton_returns_same_object():
    registry = Registry(service_configs=[SCDatabase], auto_bind=True)

    # Can find both modules even though
    assert registry.get(DatabaseConfig) is not None

    id1 = id(registry.get(DatabaseConfig))
    id2 = id(registry.get(DatabaseConfig))
    assert id1 == id2


@pytest.fixture(scope="function")
def test_non_singleton_returns_different_object():
    registry = Registry(service_configs=[SCTimestamper], auto_bind=True)

    # Can find both modules even though
    assert registry.get(TimeStamp) is not None

    id1 = id(registry.get(TimeStamp))
    id2 = id(registry.get(TimeStamp))
    assert id1 != id2
