from typing import override as _override

from leads.dt.device import Device


class Controller(Device):
    def __init__(self) -> None:
        super().__init__()
        self._devices: dict[str, Device] = {}

    def level(self) -> int:
        return len(self._parent_tags)

    def _attach_device(self, tag: str, device: Device) -> None:
        self._devices[tag] = device
        device.tag(tag)

    def devices(self) -> list[Device]:
        return list(self._devices.values())

    def device(self, tag: str, device: Device | None = None) -> Device | None:
        if device:
            self._attach_device(tag, device)
        else:
            return self._devices[tag]

    @_override
    def initialize(self, *parent_tags: str) -> None:
        for device in self._devices.values():
            device.initialize(*tuple(self._parent_tags), self._tag)
