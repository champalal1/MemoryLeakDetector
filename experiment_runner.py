import pandas as pd
import numpy as np
import os


LOG_FILE = "data/memory_logs.csv"
RESULT_FILE = "data/experiment_results.csv"


def analyze_pid(pid, test_name):

    if not os.path.exists(LOG_FILE):
        print("Memory log file not found.")
        return

    df = pd.read_csv(LOG_FILE)

    df["timestamp"] = pd.to_datetime(
        df["timestamp"]
    )

    process_data = df[
        df["pid"] == pid
    ].copy()

    if process_data.empty:
        print(f"No data found for PID {pid}")
        return

    process_data = process_data.sort_values(
        "timestamp"
    )

    memory = process_data[
        "memory_mb"
    ].values

    initial_memory = memory[0]
    final_memory = memory[-1]

    growth = (
        final_memory -
        initial_memory
    )

    duration = (
        process_data["timestamp"].iloc[-1]
        -
        process_data["timestamp"].iloc[0]
    ).total_seconds()

    if duration > 0:
        growth_rate = growth / duration
    else:
        growth_rate = 0

    x = np.arange(len(memory))

    slope = np.polyfit(
        x,
        memory,
        1
    )[0]

    print("\n======================================")
    print("        EXPERIMENT RESULT")
    print("======================================")

    print(f"Test Case       : {test_name}")
    print(f"PID             : {pid}")
    print(f"Samples         : {len(memory)}")
    print(f"Duration        : {duration:.2f} sec")
    print(f"Initial Memory  : {initial_memory:.2f} MB")
    print(f"Final Memory    : {final_memory:.2f} MB")
    print(f"Total Growth    : {growth:.2f} MB")
    print(f"Growth Rate     : {growth_rate:.4f} MB/sec")
    print(f"Trend Slope     : {slope:.4f}")

    # Simple experimental classification
    if growth > 20 and growth_rate > 0.5:
        result = "POTENTIAL_LEAK"

    elif growth > 10:
        result = "SUSPICIOUS"

    else:
        result = "NORMAL"

    print(f"Result          : {result}")

    new_result = pd.DataFrame([{
        "test_case": test_name,
        "pid": pid,
        "samples": len(memory),
        "duration_sec": round(duration, 2),
        "initial_memory_mb": round(initial_memory, 2),
        "final_memory_mb": round(final_memory, 2),
        "total_growth_mb": round(growth, 2),
        "growth_rate_mb_sec": round(growth_rate, 4),
        "trend_slope": round(slope, 4),
        "result": result
    }])

    if os.path.exists(RESULT_FILE):

        existing = pd.read_csv(
            RESULT_FILE
        )

        updated = pd.concat(
            [existing, new_result],
            ignore_index=True
        )

    else:

        updated = new_result

    updated.to_csv(
        RESULT_FILE,
        index=False
    )

    print(
        f"\nResult saved to "
        f"{RESULT_FILE}"
    )


if __name__ == "__main__":

    print("\n======================================")
    print("       EXPERIMENT RUNNER")
    print("======================================")

    pid = int(
        input("Enter PID: ")
    )

    test_name = input(
        "Enter test case name: "
    )

    analyze_pid(
        pid,
        test_name
    )
