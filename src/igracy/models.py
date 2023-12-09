from __future__ import annotations

import typing as t
from dataclasses import dataclass

T = t.TypeVar("T")


@dataclass
class InputOption(t.Generic[T]):
    value: T


@dataclass
class DeeperInputOption(InputOption[t.List[InputOption]]):
    pass


@dataclass
class UserAnyStrInputOption(InputOption[str]):
    pass


@dataclass
class UserChoiceInputOption(InputOption[t.List[t.Any]]):
    pass


@dataclass
class UserTypeInputOption(InputOption[t.List[str]]):
    pass


@dataclass
class ReplayInputOption(InputOption[t.List[str]]):
    pass


@dataclass
class UserInputParams(t.Generic[T]):
    attr_name: str
    selected_value: t.Optional[t.Any]
    options: InputOption[T]
