from typing import NewType

from src.fastinject import Registry
from test.objects_for_testing import services
from src.fastinject import Registry, inject, injectable, ServiceConfig, provider

DBConfig1 = NewType("DatabaseConfig", services.DatabaseConfig)
DBConfig2 = NewType("DatabaseConfig", services.DatabaseConfig)



def test_can_register_multiple_instances_of_same_type():

    class MyServiceConfig(ServiceConfig):
        @provider
        def provide_config1(self) -> DBConfig1:
            return services.DatabaseConfig(connection_string="constring_1")

        @provider
        def provide_config2(self) -> DBConfig2:
            return services.DatabaseConfig(connection_string="constring_2")

    registry = Registry(service_configs=[MyServiceConfig])
    assert registry.get(DBConfig1).connection_string == "constring_1"
    assert registry.get(DBConfig2).connection_string == "constring_2"
