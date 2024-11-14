import logging
import time
from typing import Type, TypeVar

from injector import ScopeDecorator, Scope, Provider

from src.fastinject import Registry, inject_from
from test.objects_for_testing import services
from test.objects_for_testing import service_configs


def test_eager_loading():
    registry = Registry(service_configs=[service_configs.SCDatabase], services=[services.TimeStamp])

    def my_func(ts: services.TimeStamp):
        pass

    inject_func = inject_from(registry=registry, inject_missing_optional_as_none=True)(my_func)
    for ding in registry._services:
        print("service", ding, type(ding))

    for ding in registry._service_configs:
        print("sc", ding, type(ding))
