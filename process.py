from dataclasses import dataclass
from enum import Enum, auto
import socket
from threading import Thread, Timer
from typing import Any
from random import choice


class State(Enum):
    DO_NOT_WANT = auto()
    WANTED = auto()
    HELD = auto()


@dataclass
class Message:
    timestamp: int
    data: Any


class Process(Thread):
    def __init__(self, port: int, pid: int, host: str = "127.0.0.1") -> None:
        super().__init__(daemon=True)
        self._port: int = port
        self._pid: int = pid
        self._host: str = host
        self._time_out: int = 5
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

    @property
    def time_out(self):
        return self._time_out

    @time_out.setter
    def time_out(self, new_time: int):
        self._time_out = new_time

    def init_socket(self):
        """
        Binds Process to an adress and starts listening for connections.
        """
        self.sock.bind((self.host, self.port))
        self.sock.listen()

    def run(self):
        """
        Overrides Thread run() method.
        """

        def update_state():
            rnd_state = choice(list(State))
            self.state = rnd_state

        while True:
            t = Timer(self.time_out, update_state)
            t.start()

    def __repr__(self) -> str:
        return f"Process(pid={self.pid}, port={self.port}, state={self.state})"
