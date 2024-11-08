from src.fastinject import Registry
from test.objects_for_testing.modules import ModuleDatabase, ModuleTimestamper
from test.objects_for_testing.services import MyDatabaseConfig, TimeStamp


def test_singleton_returns_same_object():
    registry = Registry(service_configs=[ModuleDatabase], auto_bind=True)

    # Can find both modules even though
    assert registry.get(MyDatabaseConfig) is not None

    id1 = id(registry.get(MyDatabaseConfig))
    id2 = id(registry.get(MyDatabaseConfig))
    assert id1 == id2


def test_non_singleton_returns_different_object():
    registry = Registry(service_configs=[ModuleTimestamper], auto_bind=True)

    # Can find both modules even though
    assert registry.get(TimeStamp) is not None

    id1 = id(registry.get(TimeStamp))
    id2 = id(registry.get(TimeStamp))
    assert id1 != id2
