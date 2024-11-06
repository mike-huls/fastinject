from typing import Annotated, Optional, Union
import unittest
from unittest.mock import patch, MagicMock

import src.injectr as di
import src.injectr.injection as Binder
import uuid

# from injector import Module, provider, Injector, inject
# from injector import singleton, threadlocal, noscope

from typing import NewType

ConnectionString = NewType("ConnectionString", str)

import logging, sys

logger = logging.getLogger(__name__)
# logging.basicConfig(level=logging.DEBUG)
# logging.getLogger('injector').setLevel(logging.DEBUG)


class TMyDatabaseConfig:
    def __init__(self, connection_string: str) -> None:
        self._connection_string = connection_string

    @property
    def connection_string(self) -> str:
        return self._connection_string


class Test_TestModule(di.XModule):
    @di.singleton
    @di.provider
    def provide_config(self) -> TMyDatabaseConfig:
        return TMyDatabaseConfig("file:memdb1?mode=memory&cache=shared3")


class Test_NoneModule(di.XModule):
    @di.singleton
    @di.provider
    def provide_config(
        self,
    ) -> (
        TMyDatabaseConfig
    ):  # note this must be specified to return the required type, you can't wrap it in Optional[..]
        return None


class Test_MyService:
    @di.inject
    def __init__(self, db: Optional[TMyDatabaseConfig] = None) -> None:
        self.db = db
        pass

    def get_db(self) -> Union[TMyDatabaseConfig, None]:
        return self.db


class TestInjector3(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def test_optional_params_1(self):
        """Test example"""

        # registry = di.RegistryBuilder().add_module(Test_TestModule).build()
        def configure_for_testing(binder: Binder):
            binder.bind(
                TMyDatabaseConfig,
                TMyDatabaseConfig("file:memdb1?mode=memory&cache=shared3"),
            )
            pass

        registry = di.RegistryBuilder().add_setup(configure_for_testing).build()
        service = registry.get(Test_MyService)
        self.assertEqual(service.get_db().connection_string, "file:memdb1?mode=memory&cache=shared3")

    def test_optional_params_2(self):
        """Test example"""

        def configure_for_testing(binder: Binder):
            binder.bind(
                TMyDatabaseConfig,
                TMyDatabaseConfig("file:memdb1?mode=memory&cache=shared3"),
            )
            pass

        registry = di.RegistryBuilder().add_setup(configure_for_testing).build()
        self.assertTrue(True)
        service = registry.get(Test_MyService)
        self.assertEqual(service.get_db().connection_string, "file:memdb1?mode=memory&cache=shared3")

    def test_optional_params_3(self):
        """Test example"""

        def configure_for_testing(binder: Binder):
            # needs to bind to a function to provide None, otherwise it will attempt to create the instance by itself
            binder.bind(TMyDatabaseConfig, to=lambda: None)
            pass

        registry = di.RegistryBuilder().add_setup(configure_for_testing).build()
        self.assertTrue(True)
        service = registry.get(Test_MyService)
        self.assertIsNone(service.get_db())

    def test_optional_params_4(self):
        """Test example"""

        def configure_for_testing(binder: Binder):
            # needs to bind to a function to provide None, otherwise it will attempt to create the instance by itself
            # binder.bind(Test_MyDatabaseConfig, to=lambda:None)
            pass

        registry = di.RegistryBuilder().add_setup(configure_for_testing).add_module(Test_NoneModule).build()
        self.assertTrue(True)
        service = registry.get(Test_MyService)
        self.assertIsNone(service.get_db())


if __name__ == "__main__":
    unittest.main()
