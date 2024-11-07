from typing import Annotated
import unittest
from unittest.mock import patch, MagicMock

import src.injectr as di
import uuid

# from injector import Module, provider, Injector, inject
# from injector import singleton, threadlocal, noscope

from typing import NewType

ConnectionString = NewType("ConnectionString", str)


class Test_MyDatabaseConfig:
    def __init__(self, connection_string: str) -> None:
        self._connection_string = connection_string

    @property
    def connection_string(self) -> str:
        return self._connection_string


class Test_TestModule(di.Module):
    @di.singleton
    @di.provider
    def provide_config(self) -> Test_MyDatabaseConfig:
        return Test_MyDatabaseConfig("file:memdb1?mode=memory&cache=shared2")

    @di.singleton
    @di.provider
    def provide_str(self, configuration: Test_MyDatabaseConfig) -> ConnectionString:
        return ConnectionString(configuration._connection_string)


class Test_MyService:
    @di.inject
    def __init__(self, cs: ConnectionString) -> None:
        self.cs = cs
        pass


class TestInjector2(unittest.TestCase):
    def setUp(self) -> None:
        def configure_for_testing(binder):
            pass

        self._registry = di.Registry().add_setup(configure_for_testing).add_module(Test_TestModule).build()

    def test_configuration_provided_by_module(self):
        """Test example"""
        self.assertTrue(True)
        service = self._registry.get(Test_MyService)
        self.assertEqual(service.cs, "file:memdb1?mode=memory&cache=shared2")

        # sc = self._injector.get(di.MyServiceConfig)
        # self.assertEqual(sc.get_message(), "message 01")
        # # MyService doesn't need to be registered up front
        # s = self._injector.get(di.MyService)
        # self.assertEqual(s.get_message(), "message 01")

        # self.assertIsNotNone(s.get_db())


if __name__ == "__main__":
    unittest.main()
