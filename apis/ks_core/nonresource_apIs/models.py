from __future__ import annotations

from typing import Optional
from attrs import define, field

__ALL__ = ["VersionInfo"]


@define(kw_only=True)
class VersionInfo:
    buildDate: str = field()
    compiler: str = field()
    gitCommit: str = field()
    gitMajor: str = field()
    gitMinor: str = field()
    gitTreeState: str = field()
    gitVersion: str = field()
    goVersion: str = field()
    platform: str = field()
    kubernetes: Optional[VersionInfo] = field(default=None)
