"""
Common
"""

from __future__ import annotations

import enum
import logging
from typing import Callable, Iterable


# Function
def typedstruct(cls=None, pack=None):
    """Generate typed struct"""

    def wrap(cls):
        if not hasattr(cls, "__annotations__"):
            raise TypeError("missing __annotations__")
        # Add _pack_
        if pack is not None:
            cls._pack_ = pack
        # Add _fields_
        cls._fields_ = [(k, cls.__dict__[k]) for k in cls.__annotations__]
        return cls

    if cls is None:
        return wrap
    return wrap(cls)


def _t(v):
    """Wrapper for type"""
    return v


def enum_map(reference: Iterable[enum.Enum], default: str = "Unknown") -> Callable[[int], str]:
    """Generate lookup mapping from enum (class)"""
    func = {d.value: d.name for d in reference}.get
    return lambda index: func(index, default)


def get_root_logger_name():
    """Get root logger name"""
    for logger_name in logging.root.manager.loggerDict:
        return logger_name
    return __name__
