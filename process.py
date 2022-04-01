from dataclasses import dataclass
from enum import Enum, auto
import socket
from threading import Thread
from typing import Any


class State(Enum):
    DO_NOT_WANT = auto()
    WANTED = auto()
    HELD = auto()


@dataclass
class Message:
    timestamp: int
    data: Any


class Process(Thread):
    def __init__(self, port: str, pid: int, host: str = "127.0.0.1") -> None:
        super().__init__(daemon=True)
        self._port = port
        self._pid = pid
        self._host = host
        self._state: State = State.DO_NOT_WANT
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    @property
    def port(self):
        return self._port

    @property
    def pid(self):
        return self._pid

    @property
    def host(self):
        return self._host

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, new_state: State):
        self._state = new_state

    @property
    def sock(self):
        return self._sock
