
import pandas as pd
import numpy as np

LOG_FILE = "data/memory_logs.csv"


def load_data():
    df = pd.read_csv(LOG_FILE)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["memory_mb"] = pd.to_numeric(df["memory_mb"], errors="coerce")
    df["pid"] = pd.to_numeric(df["pid"], errors="coerce")
    df = df.dropna(subset=["timestamp", "memory_mb", "pid"])
    return df


def calculate_growth_score(growth):
    if growth <= 1:
        return 0
    elif growth >= 50:
        return 30
    return (growth / 50) * 30


def calculate_consistency_score(memory):
    """Score sustained positive growth while ignoring tiny fluctuations."""
    differences = np.diff(memory)

    if len(differences) == 0:
        return 0

    # Ignore changes smaller than 0.1 MB as likely measurement noise.
    meaningful_changes = differences[np.abs(differences) >= 0.1]

    if len(meaningful_changes) == 0:
        return 0

    positive_changes = np.sum(meaningful_changes > 0)
    consistency = positive_changes / len(meaningful_changes)

    return consistency * 25


def calculate_trend_score(slope_mb_sec):
    if slope_mb_sec <= 0:
        return 0
    elif slope_mb_sec >= 1:
        return 20
    return slope_mb_sec * 20


def calculate_duration_score(duration):
    if duration < 10:
        return 0
    elif duration >= 120:
        return 15
    return (duration / 120) * 15


def calculate_rate_score(growth_rate):
    if growth_rate <= 0:
        return 0
    elif growth_rate >= 1:
        return 10
    return growth_rate * 10


def analyze_process(pid):
    df = load_data()
    process_data = df[df["pid"] == pid].copy()

    if process_data.empty:
        print(f"\nNo data found for PID {pid}")
        return

    process_data = (
        process_data.sort_values("timestamp")
        .drop_duplicates(subset=["timestamp"], keep="last")
    )

    if len(process_data) < 2:
        print(f"\nNot enough samples for PID {pid}. Need at least 2.")
        return

    memory = process_data["memory_mb"].to_numpy(dtype=float)
    timestamps = process_data["timestamp"]

    initial_memory = memory[0]
    final_memory = memory[-1]
    growth = final_memory - initial_memory
    duration = (timestamps.iloc[-1] - timestamps.iloc[0]).total_seconds()

    if duration > 0:
        growth_rate = growth / duration
        elapsed_seconds = (
            timestamps - timestamps.iloc[0]
        ).dt.total_seconds().to_numpy()

        # Linear regression using elapsed seconds, not sample index.
        slope = float(np.polyfit(elapsed_seconds, memory, 1)[0])
    else:
        growth_rate = 0.0
        slope = 0.0

    growth_score = calculate_growth_score(growth)
    consistency_score = calculate_consistency_score(memory)
    trend_score = calculate_trend_score(slope)
    duration_score = calculate_duration_score(duration)
    rate_score = calculate_rate_score(growth_rate)

    total_score = min(
        growth_score
        + consistency_score
        + trend_score
        + duration_score
        + rate_score,
        100,
    )

    if total_score <= 30:
        classification = "NORMAL"
        explanation = "Memory usage appears stable."
    elif total_score <= 40:
        classification = "LOW RISK"
        explanation = "Some memory growth detected; continue monitoring."
    elif total_score <= 60:
        classification = "SUSPICIOUS"
        explanation = "Persistent memory growth requires investigation."
    elif total_score <= 80:
        classification = "HIGH RISK"
        explanation = "Strong signs of persistent memory growth."
    else:
        classification = "POTENTIAL MEMORY LEAK"
        explanation = "Strong evidence of continuous memory growth."

    print("\n======================================")
    print("       MEMORY LEAK ANALYSIS")
    print("======================================")
    print(f"PID: {pid}")
    print(f"Process: {process_data['process_name'].iloc[0]}")
    print(f"Samples: {len(process_data)}")
    print(f"Duration: {duration:.2f} seconds")
    print(f"Initial Memory: {initial_memory:.2f} MB")
    print(f"Final Memory: {final_memory:.2f} MB")
    print(f"Total Growth: {growth:.2f} MB")
    print(f"Growth Rate: {growth_rate:.4f} MB/sec")
    print(f"Memory Trend Slope: {slope:.4f} MB/sec")

    print("\n======================================")
    print("             LEAK SCORE")
    print("======================================")
    print(f"Cumulative Growth Score : {growth_score:.2f}/30")
    print(f"Consistency Score       : {consistency_score:.2f}/25")
    print(f"Trend Score             : {trend_score:.2f}/20")
    print(f"Duration Score          : {duration_score:.2f}/15")
    print(f"Growth Rate Score       : {rate_score:.2f}/10")
    print("--------------------------------------")
    print(f"TOTAL LEAK RISK SCORE   : {total_score:.2f}/100")
    print(f"CLASSIFICATION          : {classification}")
    print(explanation)
    print("======================================\n")


if __name__ == "__main__":
    try:
        pid = int(input("Enter PID to analyze: "))
        analyze_process(pid)
    except ValueError:
        print("Please enter a valid numeric PID.")
