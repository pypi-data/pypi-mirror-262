from typing import Any, Callable, TypeVar, Generic, Union

T = TypeVar('T')


class ImmutableVariable(Generic[T]):
    def __init__(self, value: T):
        object.__setattr__(self, '_value', value)


    def __getattr__(self, name: str) -> Any:
        if hasattr(self._value, name):
            return getattr(self._value, name)
        else:
            raise AttributeError(f"{type(self._value).__name__} object has no attribute '{name}'")

    def __getitem__(self, key: Any) -> Any:
        if hasattr(self._value, '__getitem__'):
            return self._value[key]
        else:
            raise TypeError(f"{type(self._value).__name__} object is not subscriptable")

    def __setattr__(self, key: str, value: Any) -> None:
        raise AttributeError("Cannot modify immutable variable")

    def __delattr__(self, item: str) -> None:
        raise AttributeError("Cannot delete immutable variable attributes")

    def __call__(self, *args, **kwargs) -> Any:
        if callable(self._value):
            return self._value(*args, **kwargs)
        else:
            raise TypeError(f"{type(self._value).__name__} object is not callable")

