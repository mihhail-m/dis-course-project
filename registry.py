from typing import List
from process import Process


class Registry:
    def __init__(self) -> None:
        self._processes: List[Process] = []

    @property
    def processes(self):
        return self._processes

    def add_process(self, process: Process):
        self.processes.append(process)

    def list_processe(self):
        for proc in self.processes:
            print(f"PID: {proc.pid}, STATE: {proc.state.name}")

    def start_processes(self):
        for proc in self.processes:
            proc.start()
