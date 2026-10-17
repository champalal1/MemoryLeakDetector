import pandas as pd
import numpy as np


LOG_FILE = "data/memory_logs.csv"


def load_data():

    df = pd.read_csv(LOG_FILE)

    df["timestamp"] = pd.to_datetime(
        df["timestamp"]
    )

    return df


def calculate_growth_score(growth):

    if growth <= 1:
        return 0

    elif growth >= 50:
        return 30

    else:
        return (growth / 50) * 30


def calculate_consistency_score(memory):

    differences = np.diff(memory)

    if len(differences) == 0:
        return 0

    positive_changes = np.sum(
        differences > 0
    )

    consistency = (
        positive_changes /
        len(differences)
    )

    return consistency * 25


def calculate_trend_score(slope):

    if slope <= 0:
        return 0

    elif slope >= 1:
        return 20

    else:
        return slope * 20


def calculate_duration_score(duration):

    if duration < 10:
        return 0

    elif duration >= 120:
        return 15

    else:
        return (
            duration / 120
        ) * 15


def calculate_rate_score(growth_rate):

    if growth_rate <= 0:
        return 0

    elif growth_rate >= 1:
        return 10

    else:
        return growth_rate * 10


def analyze_process(pid):

    df = load_data()

    process_data = df[
        df["pid"] == pid
    ].copy()

    if process_data.empty:

        print(
            f"\nNo data found for PID {pid}"
        )

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

        growth_rate = (
            growth /
            duration
        )

    else:

        growth_rate = 0

    x = np.arange(
        len(memory)
    )

    slope = np.polyfit(
        x,
        memory,
        1
    )[0]

    # Calculate scores

    growth_score = calculate_growth_score(
        growth
    )

    consistency_score = (
        calculate_consistency_score(
            memory
        )
    )

    trend_score = calculate_trend_score(
        slope
    )

    duration_score = (
        calculate_duration_score(
            duration
        )
    )

    rate_score = calculate_rate_score(
        growth_rate
    )

    total_score = (
        growth_score
        +
        consistency_score
        +
        trend_score
        +
        duration_score
        +
        rate_score
    )

    total_score = min(
        total_score,
        100
    )

    print("\n======================================")
    print("       MEMORY LEAK ANALYSIS")
    print("======================================")

    print(
        f"\nPID: {pid}"
    )

    print(
        f"Process: "
        f"{process_data['process_name'].iloc[0]}"
    )

    print(
        f"Samples: "
        f"{len(process_data)}"
    )

    print(
        f"Duration: "
        f"{duration:.2f} seconds"
    )

    print(
        f"Initial Memory: "
        f"{initial_memory:.2f} MB"
    )

    print(
        f"Final Memory: "
        f"{final_memory:.2f} MB"
    )

    print(
        f"Total Growth: "
        f"{growth:.2f} MB"
    )

    print(
        f"Growth Rate: "
        f"{growth_rate:.4f} MB/sec"
    )

    print(
        f"Memory Trend Slope: "
        f"{slope:.4f} MB/sample"
    )

    print("\n======================================")
    print("             LEAK SCORE")
    print("======================================")

    print(
        f"Cumulative Growth Score : "
        f"{growth_score:.2f}/30"
    )

    print(
        f"Consistency Score       : "
        f"{consistency_score:.2f}/25"
    )

    print(
        f"Trend Score             : "
        f"{trend_score:.2f}/20"
    )

    print(
        f"Duration Score          : "
        f"{duration_score:.2f}/15"
    )

    print(
        f"Growth Rate Score       : "
        f"{rate_score:.2f}/10"
    )

    print("--------------------------------------")

    print(
        f"TOTAL LEAK RISK SCORE   : "
        f"{total_score:.2f}/100"
    )

    print("\n======================================")

    if total_score <= 30:

        print("✓ NORMAL")

        print(
            "Memory usage appears stable."
        )

    elif total_score <= 50:

        print("⚠ LOW RISK")

        print(
            "Some memory growth detected."
        )

    elif total_score <= 70:

        print("⚠ SUSPICIOUS")

        print(
            "Memory growth requires investigation."
        )

    elif total_score <= 85:

        print("⚠ HIGH RISK")

        print(
            "Strong signs of persistent memory growth."
        )

    else:

        print("🚨 POTENTIAL MEMORY LEAK")

        print(
            "Strong evidence of continuous memory growth."
        )

    print("======================================\n")


if __name__ == "__main__":

    pid = int(
        input(
            "Enter PID to analyze: "
        )
    )

    analyze_process(pid)
