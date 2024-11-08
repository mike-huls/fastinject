import datetime
import time

from src.injectr import inject, injectable


"""
Take the class that defines your service and mark it to be injectable with the `@injectable` decorator.
Next decorate your target function with `@inject` and the service will be automatically injected into the function!

Note: only works with services that don't need arguments to initialize with. Otherwise use the ServiceConfig (demo2)
"""


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


# todo : test singleton

if __name__ == "__main__":
    function_with_injection()
