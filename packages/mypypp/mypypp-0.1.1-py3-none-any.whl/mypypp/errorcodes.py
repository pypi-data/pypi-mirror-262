"""Copyright (c) 2024 Bendabir."""

from __future__ import annotations

from typing import Final

from mypy.errorcodes import ErrorCode

DEPRECATED: Final = ErrorCode(
    "deprecated",
    "Code is deprecated.",
    "General",
    default_enabled=True,
)
