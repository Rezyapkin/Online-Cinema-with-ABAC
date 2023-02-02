from copy import copy
from functools import wraps

from typing import Callable


def chain(func: Callable) -> Callable:
    """Creates a new instance of the class, calls a decorated method for it, and returns the instance of the class."""

    @wraps(func)
    def wrap(self, *args, **kwargs):
        new_instance = copy(self)
        func(new_instance, *args, **kwargs)
        return new_instance

    return wrap
