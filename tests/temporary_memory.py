import time
import os
import gc


print("================================")
print("    TEMPORARY MEMORY TEST")
print("================================")

print(f"PID: {os.getpid()}")

try:

    while True:

        print("\nAllocating 200 MB...")

        data = bytearray(
            200 * 1024 * 1024
        )

        time.sleep(5)

        print("Releasing memory...")

        del data

        gc.collect()

        time.sleep(5)

except KeyboardInterrupt:

    print("\nTemporary memory test stopped.")
