import socket
from threading import Lock, Thread


class CriticalSection(Thread):
    def __init__(self, host: str = "127.0.0.1", port: int = 4001) -> None:
        super().__init__(daemon=True)
        self._host = host
        self._port = port
        self._lock = Lock()
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._timeout = 10

    @property
    def host(self):
        return self._host

    @property
    def port(self):
        return self._port

    @property
    def lock(self):
        return self._lock

    @property
    def sock(self):
        return self._sock

    @property
    def timeout(self):
        return self._timeout

    @timeout.setter
    def timeout(self, new_timeout: int):
        self._timeout = new_timeout

    def _start_server(self):
        with self.sock as s:
            s.bind((self.host, self.port))
            print(f"Critical section listening on port {self.port}")
            s.listen(1)
            conn, addr = s.accept()

            with conn:
                print(f"Accepted connection from {addr}")

                while True:
                    req = conn.recv(1024)  # receive request
                    if not req:
                        break

                    # process request
                    print(f"Request: {req!r}")
                    conn.sendall(b"Request processed. Access granted.")

    def run(self) -> None:
        print("Initialized critical section.")
        try:
            self._start_server()
        except Exception as ex:
            print(ex)
        finally:
            self.sock.close()
            exit(0)
