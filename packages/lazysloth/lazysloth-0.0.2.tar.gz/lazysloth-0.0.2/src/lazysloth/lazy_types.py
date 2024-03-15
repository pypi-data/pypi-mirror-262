from typing import Callable, Generic, TypeVar
from src.lazysloth.immutable_types import ImmutableVariable

T = TypeVar('T')

class LazyVariable(Generic[T]):
    def __init__(self, initializer: Callable[..., T], *args, **kwargs):
        object.__setattr__(self, "_initializer", initializer)
        object.__setattr__(self, "_args", args)
        object.__setattr__(self, "_kwargs", kwargs)
        object.__setattr__(self, "_immutable_value", None)
        object.__setattr__(self, "_initialized", False)

    def _initialize(self) -> None:
        if not self._initialized:
            value = self._initializer(*self._args, **self._kwargs)
            object.__setattr__(self, "_immutable_value", ImmutableVariable(value))
            object.__setattr__(self, "_initialized", True)

    def __getattr__(self, item: str):
        if not self._initialized:
            self._initialize()
        if hasattr(self._immutable_value, item):
            return getattr(self._immutable_value, item)
        raise AttributeError(f"{self.__class__.__name__} object has no attribute '{item}'")

    def __getitem__(self, key):
        self._initialize()
        return self._immutable_value[key]

    def __call__(self, *args, **kwargs):
        self._initialize()
        return self._immutable_value(*args, **kwargs)

    def __setattr__(self, key, value):
        if "_initialized" in self.__dict__ and self.__dict__["_initialized"] and key not in {"_initializer", "_args", "_kwargs", "_immutable_value", "_initialized"}:
            raise AttributeError("Cannot modify attributes of a lazy immutable variable")
        super().__setattr__(key, value)

    def __delattr__(self, item):
        if "_initialized" in self.__dict__ and self.__dict__["_initialized"]:
            raise AttributeError("Cannot delete attributes of a lazy immutable variable")
        super().__delattr__(item)

