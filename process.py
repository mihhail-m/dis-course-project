from dataclasses import dataclass
from datetime import datetime
from enum import Enum, auto
import socket
from threading import Thread, Timer
from typing import Any
from random import choice, randint

from critical_section import CriticalSection


class State(Enum):
    DO_NOT_WANT = auto()
    WANTED = auto()
    HELD = auto()


@dataclass
class Message:
    data: Any
    timestamp: int = datetime.now()


class Process(Thread):
    def __init__(self, port: int, pid: int, host: str = "127.0.0.1") -> None:
        super().__init__()
        self._port: int = port
        self._pid: int = pid
        self._host: str = host
        self._time_out: int = 5
        self._state: State = State.DO_NOT_WANT
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._cs: CriticalSection = None
        self._cs_access: bool = False
        self._neighbours: list[Process] = []
        self._timestamp = datetime.now()
        self._server_mode = False
        self._running = True

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
    def time_out(self, new_max_timeout: int):
        """
        Sets new upper bound for timeout's interval.
        Lower bound by default is 5 seconds.

        Args:
            new_max_timeout (int): Interval's upper bound in seconds.
        """
        self._time_out = randint(5, new_max_timeout)

    @property
    def critical_section(self):
        return self._cs

    @critical_section.setter
    def critical_section(self, cs: CriticalSection):
        self._cs = cs

    @property
    def has_cs_access(self):
        return self._cs_access

    @has_cs_access.setter
    def has_cs_access(self, access: bool):
        self._cs_access = access

    @property
    def neighbours(self):
        return self._neighbours

    @neighbours.setter
    def add_neighbour(self, neighbours):
        filtered_n = list(filter(lambda n: n.pid != self.pid, neighbours))
        self._neighbours = filtered_n

    @property
    def timestamp(self):
        return self._timestamp

    def stop(self):
        self._running = False

    def start_server_mode(self):
        """
        Binds Process to an adress and starts listening for connections.
        """
        state = self.state
        with self.sock as s:
            s.bind((self.host, self.port))
            s.listen(len(self.neighbours))
            conn, addr = s.accept()

            with conn:
                print(f"Connected from {addr}")

                while True:
                    data = conn.recv(1024)

                    if not data:
                        print("No data has been received.")
                        break

                    if state == State.WANTED:
                        # compare timestamps
                        conn.sendall(b"WANTED")
                    elif state == State.HELD:
                        conn.sendall(b"HELD")
                    else:
                        conn.sendall(b"OK")

    def send_message(self, sock, port: int, data: Any, host: str = "127.0.0.1"):
        with self.sock as s:
            s.connect((host, port))
            s.sendall(data)
            res = s.recv(1024)

            if "OK" in repr(res):
                return "Granted"

        return "Denied"

    def request_cs(self):
        """
        Sends request to access Critical Section.
        """
        if self.critical_section is None:
            raise ValueError("Critical Section is not specified.")

        cs_host = self.critical_section.host
        cs_port = self.critical_section.port

        with self.sock as s:
            print("Sending request to Critical Section.")
            s.connect((cs_host, cs_port))
            s.send(b"Request")

            res = s.recv(1024)

            print(f"Received: {res!r}")

    def run(self):
        def update_state():
            rnd_state = choice([State.DO_NOT_WANT, State.WANTED])
            self.state = rnd_state

        while self._running:
            try:
                t = Timer(self.time_out, update_state)
                t.setDaemon(True)
                t.start()
            except Exception as ex:
                print(ex)
                exit(1)

    def __repr__(self) -> str:
        return f"Process(pid={self.pid}, port={self.port}, state={self.state})"
