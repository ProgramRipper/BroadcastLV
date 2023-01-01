import re

__all__ = ("pascal_to_upper_snake",)


def pascal_to_upper_snake(name: str) -> str:
    return re.sub(r"(?<!^)(?=[A-Z])", "_", name).upper()
