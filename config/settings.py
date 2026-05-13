"""Backward-compatible settings module.

Some modules import `config.settings` while the actual file is
`config/setting.py`. This bridge re-exports everything from
`.setting` so both import styles continue to work.
"""

from .setting import *

__all__ = [name for name in dir() if not name.startswith("_")]
