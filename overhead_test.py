import subprocess
import time
import psutil


MONITOR_COMMAND = ["python", "main.py"]
DURATION = 60


def main():

    print("\n======================================")
    print("       MONITORING OVERHEAD TEST")
    print("======================================")

    print("\nStarting memory monitoring system...")

    process = subprocess.Popen(
        MONITOR_COMMAND
    )

    monitor = psutil.Process(
        process.pid
    )

    cpu_samples = []
    memory_samples = []

    print(
        f"Monitor PID: {process.pid}"
    )

    print(
        f"Testing for {DURATION} seconds..."
    )

    start_time = time.time()

    try:

        while (
            time.time() - start_time
            < DURATION
        ):

            try:

                cpu = monitor.cpu_percent(
                    interval=1
                )

                memory = (
                    monitor.memory_info().rss
                    / (1024 * 1024)
                )

                cpu_samples.append(cpu)
                memory_samples.append(memory)

                print(
                    f"CPU: {cpu:6.2f}% | "
                    f"RAM: {memory:7.2f} MB"
                )

            except psutil.NoSuchProcess:

                print(
                    "Monitor process stopped."
                )

                break

    except KeyboardInterrupt:

        print(
            "\nTest interrupted."
        )

    finally:

        if process.poll() is None:

            process.terminate()

            try:
                process.wait(
                    timeout=5
                )

            except subprocess.TimeoutExpired:

                process.kill()

    if not cpu_samples:

        print(
            "\nNo monitoring data collected."
        )

        return

    average_cpu = (
        sum(cpu_samples)
        /
        len(cpu_samples)
    )

    maximum_cpu = max(
        cpu_samples
    )

    average_memory = (
        sum(memory_samples)
        /
        len(memory_samples)
    )

    maximum_memory = max(
        memory_samples
    )

    minimum_memory = min(
        memory_samples
    )

    print("\n======================================")
    print("        OVERHEAD TEST RESULT")
    print("======================================")

    print(
        f"\nAverage CPU Usage : "
        f"{average_cpu:.2f}%"
    )

    print(
        f"Maximum CPU Usage : "
        f"{maximum_cpu:.2f}%"
    )

    print(
        f"Average RAM Usage : "
        f"{average_memory:.2f} MB"
    )

    print(
        f"Maximum RAM Usage : "
        f"{maximum_memory:.2f} MB"
    )

    print(
        f"Minimum RAM Usage : "
        f"{minimum_memory:.2f} MB"
    )

    print("\n======================================")
    print("              TEST COMPLETE")
    print("======================================\n")


if __name__ == "__main__":
    main()
