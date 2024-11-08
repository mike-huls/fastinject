import datetime
import time

from injector import singleton

from src.fastinject import inject, set_default_registry, get_default_registry, injectable
# from test.objects_for_testing.services_injectable import TimeStamp


def test_injectable_servcie_is_injectable():
    @injectable()
    class TimeStamp:
        ts: float

        def __init__(self) -> None:
            self.ts = time.time()

        @property
        def datetime_str(self) -> str:
            return datetime.datetime.fromtimestamp(self.ts).strftime("%Y-%m-%d %H:%M:%S")

    @inject()
    def function_with_injection(ts: TimeStamp):
        print(f"In the injected function, the current time is {ts.datetime_str}.")
        assert ts is not None

    # set_default_registry(registry=None)
    function_with_injection()
    reg = get_default_registry()
    print(reg.get(TimeStamp))
    print(reg.get(TimeStamp))


def test_injectable_service_is_not_singleton():
    @injectable()
    class _TimeStamp:
        ts: float

        def __init__(self) -> None:
            self.ts = time.time()

    @inject()
    def function_with_injection(ts: _TimeStamp):
        id_1 = id(ts)
        ts_1 = ts.ts

        print(id(ts), ts.ts)

        @inject()
        def other_function_with_injection(ts: _TimeStamp):
            print(id(ts), ts.ts)
            assert id(ts) != id_1
            assert ts.ts != ts_1

        time.sleep(0.1)
        other_function_with_injection()

    # set_default_registry(registry=None)
    reg = get_default_registry()
    print(id(reg.get(_TimeStamp)))
    print(id(reg.get(_TimeStamp)))
    function_with_injection()


def test_injectable_servcie_singleton_works():
    @injectable(scope=singleton)
    class TimeStamp:
        ts: float

        def __init__(self) -> None:
            self.ts = time.time()

    @inject()
    def function_with_injection(ts: TimeStamp):
        id_1 = id(ts)
        ts_1 = ts.ts

        print(id(ts), ts.ts)

        @inject()
        def other_function_with_injection(ts: TimeStamp):
            print(id(ts), ts.ts)
            assert id(ts) == id_1
            assert ts.ts == ts_1

        time.sleep(0.1)
        other_function_with_injection()

    # set_default_registry(registry=None)
    function_with_injection()
