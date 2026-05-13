"""Config package initializer."""

from .setting import *

__all__ = [name for name in dir() if not name.startswith("_")]
