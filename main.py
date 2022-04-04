import sys
from critical_section import CriticalSection
from process import Process
from registry import Registry


registry = Registry()
critical_section = CriticalSection()


def main():
    n_processes = int(input("Number of process to run> "))

    if n_processes < 1:
        raise ValueError("Number of processes must be more than 0.")

    # Creating processes
    for i in range(n_processes):
        proc = Process(pid=i, port=3000 + i)
        registry.add_process(proc)

    running = True

    # Initialisation
    critical_section.start()
    registry.set_neighbours()
    registry.set_critical_section(critical_section)
    registry.start_processes()

    while running:
        user_inp = input("Insert command> ").lower()
        user_inp = user_inp.split(" ")
        cmd = user_inp[0]

        if cmd == "list":
            registry.list_processes()

        elif cmd == "time-p":
            new_max_timeout = int(user_inp[1])
            registry.set_timeout(new_max_timeout)

        elif cmd == "time-cs":
            new_cs_timeout = int(user_inp[1])
            critical_section.timeout = new_cs_timeout

        elif cmd == "neighbours":
            registry.show_neighbours()

        elif cmd == "exit":
            print("Termintated programm.")
            registry.stop_processes()
            registry.close_connections()
            sys.exit(0)

        else:
            raise ValueError("Unsupported command.")


if __name__ == "__main__":
    main()
