from typing import override as _override

from serial import Serial as _Serial

from leads import Controller as _Controller, get_controller as _get_controller, SFT as _SFT
from leads.comm import Entity as _Entity, Callback as _Callback, Service as _Service
from leads_comm_serial import SerialConnection as _SerialConnection


class ArduinoProto(_Controller, _Entity):
    """
    Supports:
    - Any arduino connected through a USB (serial) port
    """
    def __init__(self, port: str, callback: _Callback, baud_rate: int = 9600) -> None:
        _Controller.__init__(self)
        _Entity.__init__(self, -1, callback)
        self._serial: _Serial = _Serial()
        self._serial.port = port
        self._serial.baudrate = baud_rate
        self._connection: _SerialConnection | None = None

    @_override
    def port(self) -> str:
        return self._serial.port

    @_override
    def initialize(self, *parent_tags: str) -> None:
        self.start(True)
        super().initialize(*parent_tags)

    @_override
    def update(self, data: str) -> None:
        for d in self.devices():
            d.update(data)

    @_override
    def run(self) -> None:
        self.callback.on_initialize(self)
        self._serial.open()
        self.callback.on_connect(self, connection := _SerialConnection(self, self._serial, self._serial.port))
        self._connection = connection
        self._stage(connection)

    @_override
    def write(self, payload: bytes) -> None:
        if not self._connection:
            raise IOError("Target must be connected to perform this operation")
        self._connection.send(payload)

    @_override
    def kill(self) -> None:
        if self._connection:
            self._connection.close()

    @_override
    def close(self) -> None:
        self.kill()


class ArduinoCallback(_Callback):
    def __init__(self, tag: str) -> None:
        self._tag: str = tag

    @_override
    def on_receive(self, service: _Service, msg: bytes) -> None:
        _get_controller(self._tag).update(msg.decode())

    @_override
    def on_fail(self, service: _Service, error: Exception) -> None:
        assert isinstance(service, ArduinoProto)
        _SFT.fail(service, error)
