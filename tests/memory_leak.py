import time


memory_blocks = []

print("Memory leak test started.")
print("PID:", __import__("os").getpid())

while True:

    # Allocate approximately 1 MB
    block = bytearray(1024 * 1024)

    # Keep reference to the block
    # so Python does not release it
    memory_blocks.append(block)

    print(
        f"Allocated blocks: "
        f"{len(memory_blocks)} MB"
    )

    time.sleep(1)
