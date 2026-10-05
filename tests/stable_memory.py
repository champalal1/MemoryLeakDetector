import time
import os


data = bytearray(20 * 1024 * 1024)

print("================================")
print("     STABLE MEMORY TEST")
print("================================")

print(f"PID: {os.getpid()}")

print("Allocated: 20 MB")
print("Memory should remain relatively stable.")

try:

    while True:

        time.sleep(1)

except KeyboardInterrupt:

    print("\nStable memory test stopped.")
