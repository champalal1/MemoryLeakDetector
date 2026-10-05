import time

from monitor import get_process_memory
from logger import initialize_log, log_memory


initialize_log()


print("======================================")
print("     MEMORY LEAK DETECTION SYSTEM")
print("======================================")

print("\nStarting memory monitoring...")
print("Monitoring interval: 1 second")
print("Press Ctrl+C to stop.\n")


try:

    while True:

        processes = get_process_memory()

        # Sort processes by memory usage
        processes.sort(
            key=lambda x: x["memory"],
            reverse=True
        )

        # Monitor top 10 processes
        for process in processes[:10]:

            memory_mb = process["memory"] / (1024 ** 2)

            log_memory(
                process["pid"],
                process["name"],
                memory_mb
            )

        # Display top 5 processes
        print("\n===== CURRENT MEMORY USAGE =====")

        for process in processes[:5]:

            memory_mb = process["memory"] / (1024 ** 2)

            print(
                f"PID: {process['pid']:>6} | "
                f"{process['name']:<25} | "
                f"{memory_mb:>8.2f} MB"
            )

        time.sleep(1)


except KeyboardInterrupt:

    print("\n\nMonitoring stopped.")
    print("Memory data saved to:")
    print("data/memory_logs.csv")
