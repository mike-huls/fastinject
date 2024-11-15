from injector import provider, singleton

from src.fastinject import Registry
from src.fastinject.service_config import ServiceConfig
from test.objects_for_testing import services
from test.objects_for_testing.services import TimeStamp


def test_singleton_returns_same_object():
    class SCTimestamper(ServiceConfig):
        @singleton
        @provider
        def provide_timestamper(self) -> services.TimeStamp:
            return services.TimeStamp()

    registry = Registry(service_configs=[SCTimestamper], auto_bind=True)

    # Can find both modules even though
    assert registry.get(TimeStamp) is not None


def test_non_singleton_returns_different_object():
    class SCTimestamper(ServiceConfig):
        @provider
        def provide_timestamper(self) -> services.TimeStamp:
            return services.TimeStamp()

    registry = Registry(service_configs=[SCTimestamper], auto_bind=True, auto_validate=False)

    # Can find both modules even though
    assert registry.get(TimeStamp) is not None

    id1 = id(registry.get(TimeStamp))
    id2 = id(registry.get(TimeStamp))
    print(id1)
    print(id2)
    assert id1 != id2
