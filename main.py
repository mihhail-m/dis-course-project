import sys
from process import Process
from registry import Registry

CRITICAL_SECTION = []

PROCESS_REGISTRY = Registry()


def main():
    n_processes = int(input("Number of process to run> "))

    if n_processes < 1:
        raise ValueError("Number of processes must be more than 0.")

    for i in range(n_processes):
        proc = Process(0, i)
        PROCESS_REGISTRY.add_process(proc)

    running = True

    PROCESS_REGISTRY.start_processes()

    while running:
        user_inp = input("Insert command> ").lower()

        if user_inp == "list":
            PROCESS_REGISTRY.list_processe()
        elif user_inp == "exit":
            print("Termintated programm.")
            sys.exit(0)


if __name__ == "__main__":
    main()
