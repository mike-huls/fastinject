from injector import Injector
from injector import Scope, ScopeDecorator
from typing import Any, Generic, TypeVar, Type, Union, Callable  # , Self,  Iterable
from injector import T
import logging


class Registry:
    def __init__(self, injector: Injector) -> None:
        self._injector = injector

    def setLogLevel(self, level: int) -> None:
        logging.getLogger("injector").setLevel(level)

    def get(self, interface: Type[T], scope: Union[ScopeDecorator, Type[Scope], None] = None) -> T:
        """
        Gets an instance of T and if it is decorated with @inject or any of the __init__ arguments are wrapped with Inject[...] the dependencies will be injected
        """
        return self._injector.get(interface, scope)

    def call_with_injection(
        self,
        callable: Callable[..., T],
        self_: Any = None,
        args: Any = (),  # TODO MUTABLE
        kwargs: Any = {},  # TODO MUTABLE
    ) -> T:
        """
        Calls the function and injects the parameters if the function is decorated with @inject or any of the arguments are wrapped with Inject[..]
        """
        return self._injector.call_with_injection(callable, self_, args, kwargs)
