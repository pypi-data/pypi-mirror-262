from typing import *
from functools import update_wrapper

T = TypeVar("T")


class classproperty(Generic[T]):
    """
    Chaining `@classmethod` and `@property` is ... baffling... deprecated
    in Python 3.11+, with no actual official replacement other than the
    suggestion:

      To "pass-through" a classmethod, consider using the __wrapped__ attribute
      that was added in Python 3.10.

    Umm... okay... so I guess we're writing this language feature ourselves.
    This is a simple property descriptor for read-only class properties.
    Adapted from https://stackoverflow.com/questions/76378373
    """

    def __init__(self, method: Callable[..., T]):
        self.method = method
        update_wrapper(self, method)

    def __get__(self, obj, cls=None) -> T:
        if cls is None:
            cls = type(obj)
        return self.method(cls)
