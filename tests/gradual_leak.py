import time
import os


memory_blocks = []

print("================================")
print("     GRADUAL MEMORY LEAK TEST")
print("================================")

print(f"PID: {os.getpid()}")

try:

    while True:

        # Allocate 256 KB every second
        block = bytearray(
            256 * 1024
        )

        memory_blocks.append(block)

        print(
            f"Allocated approximately "
            f"{len(memory_blocks) * 0.25:.2f} MB"
        )

        time.sleep(1)

except KeyboardInterrupt:

    print("\nGradual leak test stopped.")
