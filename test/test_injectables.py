from src.injectr import inject, set_default_registry, get_default_registry
from test.objects_for_testing.services_injectable import TimeStamp


@inject()
def function_with_injection(ts: TimeStamp):
    print(f"In the injected function, the current time is {ts.datetime_str}.")

def test_fn_injectable():
    # set_default_registry(registry=None)
    function_with_injection()
    reg = get_default_registry()
    print(reg.get(TimeStamp))
    print(reg.get(TimeStamp))

