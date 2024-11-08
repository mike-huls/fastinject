from typing import Any, Optional
from src.fastinject import inject, injectable, ServiceConfig, singleton, provider

""" 
If you have services that need arguments to be inialized or services that are dependent on other services you need the ServiceConfig.
This is a class that specifies how injectable services are initialized. 

Below the LabelPrinter service needs to be initialized with a label. In the ServiceConfig we specify how to initialize it. 

"""


# region Services
@injectable()
class LabelPrinter:
    label: Optional[str]

    def __init__(self, label: Optional[Any] = None) -> None:
        self.label = label if label is not None else None

    def print(self, *args):
        msg = " ".join(args)
        print(f"{self.label}: {msg}")


# endregion


@injectable()
class MyServiceConfig(ServiceConfig):
    @singleton
    @provider
    def provide_label_printer(self) -> LabelPrinter:
        # Here we specify how to instantiate the servcie and with what arguments. We can reference an environment variable here as wel e.g.
        return LabelPrinter(label="MY_APP")


@inject()
def function_with_injection(lp: LabelPrinter):
    lp.print("hello from the injected function")


if __name__ == "__main__":
    function_with_injection()
