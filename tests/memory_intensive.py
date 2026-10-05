import time
import gc
import os

print("======================================")
print("      MEMORY INTENSIVE WORKLOAD")
print("======================================")

print(f"PID: {os.getpid()}")

blocks = []

try:

    while True:

        print("\nAllocating 100 MB...")

        block = bytearray(
            100 * 1024 * 1024
        )

        blocks.append(block)

        time.sleep(5)

        print("Releasing memory...")

        blocks.clear()

        gc.collect()

        time.sleep(5)

except KeyboardInterrupt:

    print("\nMemory-intensive test stopped.")
