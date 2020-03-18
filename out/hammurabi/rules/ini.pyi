import abc
from abc import abstractmethod
from hammurabi.rules.common import SinglePathRule as SinglePathRule
from pathlib import Path
from typing import Any, Iterable, Optional, Tuple

class SingleConfigFileRule(SinglePathRule, metaclass=abc.ABCMeta):
    section: Any = ...
    updater: Any = ...
    def __init__(self, name: str, path: Optional[Path]=..., section: Optional[str]=..., **kwargs: Any) -> Any: ...
    def pre_task_hook(self) -> None: ...
    @abstractmethod
    def task(self) -> Any: ...

class SectionExists(SingleConfigFileRule):
    target: Any = ...
    options: Any = ...
    add_after: Any = ...
    space: int = ...
    def __init__(self, name: str, path: Optional[Path]=..., target: Optional[str]=..., options: Iterable[Tuple[str, Any]]=..., add_after: bool=..., **kwargs: Any) -> Any: ...
    def task(self) -> Path: ...

class SectionNotExists(SingleConfigFileRule):
    def task(self) -> Path: ...

class SectionRenamed(SingleConfigFileRule):
    new_name: Any = ...
    def __init__(self, name: str, path: Optional[Path]=..., new_name: Optional[str]=..., **kwargs: Any) -> Any: ...
    def task(self) -> Path: ...

class OptionsExist(SingleConfigFileRule):
    options: Any = ...
    force_value: Any = ...
    def __init__(self, name: str, path: Optional[Path]=..., options: Iterable[Tuple[str, Any]]=..., force_value: bool=..., **kwargs: Any) -> Any: ...
    def task(self) -> Path: ...

class OptionsNotExist(SingleConfigFileRule):
    options: Any = ...
    def __init__(self, name: str, path: Optional[Path]=..., options: Iterable[str]=..., **kwargs: Any) -> Any: ...
    def task(self) -> Path: ...

class OptionRenamed(SingleConfigFileRule):
    option: Any = ...
    new_name: Any = ...
    def __init__(self, name: str, path: Optional[Path]=..., option: Optional[str]=..., new_name: Optional[str]=..., **kwargs: Any) -> Any: ...
    def task(self) -> Path: ...
