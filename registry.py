from typing import List
from critical_section import CriticalSection
from process import Process


class Registry:
    def __init__(self) -> None:
        self._processes: List[Process] = []

    @property
    def processes(self):
        return self._processes

    def add_process(self, process: Process):
        self.processes.append(process)

    def list_processes(self):
        for proc in self.processes:
            print(
                f"PID: {proc.pid}, STATE: {proc.state.name}, TIMEOUT: {proc.time_out}"
            )

    def start_processes(self):
        for proc in self.processes:
            proc.start()

    def set_timeout(self, max_timeout: int):
        for proc in self.processes:
            proc.time_out = max_timeout

    def terminate_processes(self):
        for proc in self.processes:
            proc.join()

    def set_critical_section(self, cs: CriticalSection):
        for proc in self.processes:
            proc.critical_section = cs

    def set_neighbours(self):
        for proc in self.processes:
            proc.add_neighbour = self.processes

    def show_neighbours(self):
        for proc in self.processes:
            print(proc.pid, proc.neighbours)

    def close_connections(self):
        for proc in self.processes:
            proc.sock.close()

    def stop_processes(self):
        for proc in self.processes:
            proc.stop()
