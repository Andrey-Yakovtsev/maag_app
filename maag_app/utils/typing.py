from collections.abc import MutableSequence
from typing import TypeVar

_T = TypeVar("_T", int, float, str)
Array = MutableSequence[_T]
