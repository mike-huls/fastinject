import logging
import unittest
from typing import NewType, List

from src.injectr import (
    inject_services as inject_from,
    set_default_registry,
    RegistryDEPRECATED,
    Registry,
)
from test.objects_for_testing.registries import RegDatabaseLogging
from test.objects_for_testing.services import MyDatabaseConfig

ConnectionString = NewType("ConnectionString", str)


# Create registry


class TestInjectorInjectFromDefaultRegistry(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def test_inject_from_works(self):
        """Test example"""
        # 1. Create registry
        registry_builder = Registry.create()
        registry_builder.add_module(RegDatabaseLogging)
        registry: RegistryDEPRECATED = registry_builder.build()
        # we can manually set set_default_registry, but it should be populated by the .build() if it was None
        # set_default_registry(registry)
        registry = None

        @inject_from(registry=registry)
        def inject_logger_in_fn(logger: logging.Logger):
            assert logger is not None

        inject_logger_in_fn()

        @inject_from(registry=registry)
        def inject_dbconfig_in_fn(dbcon: MyDatabaseConfig):
            assert dbcon is not None
            assert dbcon.connection_string == "file:memdb1?mode=memory&cache=shared3"

        inject_dbconfig_in_fn()

        @inject_from(registry=registry)
        def inject_both(dbcon: MyDatabaseConfig, logger: logging.Logger):
            assert dbcon is not None
            assert dbcon.connection_string == "file:memdb1?mode=memory&cache=shared3"
            assert logger is not None

        inject_both()

        # Cannot get type form container that isn't registered; throws
        @inject_from(registry=registry)
        def inject_non_existent(logger: List):
            assert logger is None

        with self.assertRaises(Exception):
            inject_non_existent()

        set_default_registry(None)


if __name__ == "__main__":
    unittest.main()
