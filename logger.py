import csv
import os
from datetime import datetime


LOG_FILE = "data/memory_logs.csv"


def initialize_log():

    os.makedirs("data", exist_ok=True)

    if not os.path.exists(LOG_FILE):

        with open(LOG_FILE, "w", newline="") as file:

            writer = csv.writer(file)

            writer.writerow([
                "timestamp",
                "pid",
                "process_name",
                "memory_mb"
            ])


def log_memory(pid, process_name, memory_mb):

    with open(LOG_FILE, "a", newline="") as file:

        writer = csv.writer(file)

        writer.writerow([
            datetime.now().isoformat(),
            pid,
            process_name,
            round(memory_mb, 2)
        ])
