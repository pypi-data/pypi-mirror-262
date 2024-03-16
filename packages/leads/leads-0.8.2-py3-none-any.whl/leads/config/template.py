from json import dumps as _dumps
from typing import Any as _Any, override as _override

from leads.data import Serializable


class ConfigTemplate(Serializable):
    def __init__(self, base: dict[str, _Any]) -> None:
        """
        All custom columns should be public (not named after "_").
        :param base: base dictionary
        """
        self._d: dict[str, _Any] = base
        self.debug_level: str = "DEBUG"
        self.srw_mode: bool = True
        self.refresh()

    def __getitem__(self, name: str) -> _Any | None:
        return self.get(name)

    def __getattr__(self, name: str) -> _Any | None:
        return self.get(name)

    def __setitem__(self, name: str, value: _Any) -> None:
        self._d[name] = value
        self.refresh()

    @_override
    def __str__(self) -> str:
        return _dumps(self.to_dict())

    def load(self, d: dict[str, _Any]) -> None:
        """
        Load a new dictionary and refresh.
        :param d: the dictionary to load
        """
        self._d = d
        self.refresh()

    def get(self, name: str, default: _Any | None = None) -> _Any:
        """
        Get the value of a given name from the dictionary.
        :param name: dictionary key
        :param default: default value if the value does not exist
        :return: the value if it exists or else the default value
        """
        if r := self._d.get(name):
            return r
        return default

    def refresh(self) -> None:
        """
        Write the dictionary into the instance attributes.
        """
        for name in dir(self):
            if not name.startswith("_") and (v := self.get(name)) is not None:
                setattr(self, name, v)
