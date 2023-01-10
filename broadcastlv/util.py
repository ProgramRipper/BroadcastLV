from __future__ import annotations

import re

__all__ = [
    "pascal_to_snake",
    "pascal_to_upper_snake",
]


def pascal_to_upper_snake(name: str) -> str:
    return re.sub(r"(?<!^)(?=[A-Z])", "_", name).upper()


def pascal_to_snake(name: str) -> str:
    return re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()
