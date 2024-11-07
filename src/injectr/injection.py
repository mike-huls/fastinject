import logging
from typing import Any, Type, Union, Callable, List, Optional  # , Self,  Iterable

from injector import Injector, Binder
from injector import Module
from injector import Scope, ScopeDecorator
from injector import T

# _InstallableModuleType = Union[Callable[['XBinder'], None], 'Module', Type['Module']]
_InstallableModuleType = Union["Module", Type["Module"]]


# class XBinder(Binder):
#     def __init__(self, parent: Binder) -> None:
#         self._parent = parent
#
#     def bind(
#         self,
#         interface: Type[T],
#         to: Union[None, T, Callable[..., T], Provider[T]] = None,
#         scope: Union[None, Type["Scope"], "ScopeDecorator"] = None,
#     ) -> None:
#         self._parent.bind(interface, to, scope)



class Registry:
    def __init__(self, modules: Optional[List[_InstallableModuleType]]=None, auto_bind:bool=False) -> None:
        """
        auto_bind: bool : if True; will automatically resolve types that it can construct. Looks in all functions decorated with @provider.

        """
        #  modifier:Callable[[Registry, Injector], None] = None
        self._auto_bind = auto_bind
        # self._modifiers: list[Callable[[RegistryDEPRECATED, Injector], None]] = []
        self._modules: list[Module] = []
        self._callables: list[Callable[[Binder], None]] = []
        for module in modules or []:
            self.add_module(module=module)
        self.build()

    def __str__(self):
        return f"<Registry with modules: {self._modules}>"


    # def disable_autobind(self) -> "RegistryBuilder":
    #     self._auto_bind = False
    #     return self

    def add_module(self, module: _InstallableModuleType) -> "Registry":
        self._modules.append(module)
        self.build()
        return self

    def add_setup(self, setup_function: Callable[[Binder], None]) -> "Registry":
        self._callables.append(setup_function)
        self.build()
        return self

    # def bind(
    #     self,
    #     interface: Type[T],
    #     to: Union[None, T, Callable[..., T], Provider[T]] = None,
    #     scope: Union[None, Type["Scope"], "ScopeDecorator"] = None,
    # ) -> "T":
    #     return self.add_setup(lambda binder: binder.bind(interface, to, scope))

    def build(self) -> "Registry":

        def configure(binder: Binder):
            # dnx_bind = Binder(binder)
            for fn in self._callables:
                fn(binder)

        # setup:ParentListList = [configure]
        setup: List[Callable] = [configure]
        for m in self._modules:
            setup.append(m)

        # self._injector = Injector([configure_for_testing, di.TestModule()])
        self._injector = Injector(setup, auto_bind=self._auto_bind)
        set_default_registry(registry=self)
        return self
        # result = RegistryDEPRECATED(self._injector)
        # for modifier in self._modifiers:
        #     # if self._modifier:
        #     modifier(result, self._injector)

        # auto register the first registry as default registry
        # if get_default_registry() is None:
        #     set_default_registry(result)
        # return result

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
        args: Optional[Any]=None,
        kwargs: Optional[Any]=None,
    ) -> T:
        """
        Calls the function and injects the parameters if the function is decorated with @inject or any of the arguments are wrapped with Inject[..]
        """
        return self._injector.call_with_injection(callable, self_, args, kwargs)

__default_registry: Optional[Registry] = None

def set_default_registry(registry: Registry):
    global __default_registry
    __default_registry = registry


def get_default_registry() -> Registry:
    return __default_registry
