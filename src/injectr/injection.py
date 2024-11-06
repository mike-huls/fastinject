from injector import (
    Injector as ParentInjector,
    Binder as ParentBinder,
    Provider,
    Module as ParentModule,
)
from injector import Scope, ScopeDecorator
from typing import Any, Generic, TypeVar, Type, Union, Callable, List, Optional  # , Self,  Iterable
from injector import T
import logging
from .default_registry import Registry
from .module import XModule
from .decorators import get_default_registry, set_default_registry

# _InstallableModuleType = Union[Callable[['Binder'], None], 'Module', Type['Module']]
_InstallableModuleType = Union["XModule", Type["XModule"]]


class Binder:
    def __init__(self, parent: ParentBinder) -> None:
        self._parent = parent

    def bind(
        self,
        interface: Type[T],
        to: Union[None, T, Callable[..., T], Provider[T]] = None,
        scope: Union[None, Type["Scope"], "ScopeDecorator"] = None,
    ) -> None:
        self._parent.bind(interface, to, scope)



class RegistryBuilder:
    def __init__(self, modules: Optional[List[_InstallableModuleType]]=None) -> None:
        #  modifier:Callable[[Registry, ParentInjector], None] = None
        self._auto_bind = True
        self._modifiers: list[Callable[[Registry, ParentInjector], None]] = []
        self._modules: list[XModule] = []
        self._callables: list[Callable[[Binder], None]] = []
        for module in modules or []:
            self.add_module(module=module)
        pass

    @staticmethod
    def create():
        return RegistryBuilder()

    # def disable_autobind(self) -> "RegistryBuilder":
    #     self._auto_bind = False
    #     return self

    def add_module(self, module: _InstallableModuleType) -> "RegistryBuilder":
        self._modules.append(module)
        return self

    def add_setup(self, setup_function: Callable[[Binder], None]) -> "RegistryBuilder":
        self._callables.append(setup_function)
        return self

    def bind(
        self,
        interface: Type[T],
        to: Union[None, T, Callable[..., T], Provider[T]] = None,
        scope: Union[None, Type["Scope"], "ScopeDecorator"] = None,
    ) -> "T":
        return self.add_setup(lambda binder: binder.bind(interface, to, scope))

    def build(self) -> Registry:
        callables = self._callables

        def configure(binder: ParentBinder):
            dnx_bind = Binder(binder)
            for fn in callables:
                fn(dnx_bind)

        # setup:ParentListList = [configure]
        setup: List[Callable] = [configure]
        for m in self._modules:
            setup.append(m)

        # self._injector = ParentInjector([configure_for_testing, di.TestModule()])
        injector = ParentInjector(setup, auto_bind=self._auto_bind)
        result = Registry(injector)
        for modifier in self._modifiers:
            # if self._modifier:
            modifier(result, injector)

        # auto register the first registry as default registry
        if get_default_registry() is None:
            set_default_registry(result)
        return result

