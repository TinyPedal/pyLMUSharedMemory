"""
Common
"""

from __future__ import annotations

import enum
import logging
import mmap
import sys
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


# mmap
def platform_mmap(name: str, size: int) -> mmap.mmap:
    """Platform memory mapping"""
    if sys.platform == "win32":
        return windows_mmap(name, size)
    return linux_mmap(name, size)


def windows_mmap(name: str, size: int) -> mmap.mmap:
    """Windows mmap"""
    return mmap.mmap(-1, size, name)


def linux_mmap(name: str, size: int) -> mmap.mmap | None:
    """Linux mmap - read data from '/dev/shm/filename' if available"""
    with open(f"/dev/shm/{name}", "a+b") as file:
        stream_pos = file.tell()
        if stream_pos == 0:  # file is empty
            file.write(b"\0" * size)
            file.flush()
        elif stream_pos != size:  # file size doesn't match struct size
            file.seek(0)
            file.truncate(0)  # clear all data
            file.seek(0)
            file.write(b"\0" * size)
            file.flush()
        return mmap.mmap(file.fileno(), size)
