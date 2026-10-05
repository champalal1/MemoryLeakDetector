import pandas as pd
import matplotlib.pyplot as plt
import sys


LOG_FILE = "data/memory_logs.csv"


def visualize_process(pid):

    df = pd.read_csv(LOG_FILE)

    df["timestamp"] = pd.to_datetime(
        df["timestamp"]
    )

    process_data = df[
        df["pid"] == pid
    ].copy()

    if process_data.empty:

        print(
            f"No data found for PID {pid}"
        )

        return

    process_data = process_data.sort_values(
        "timestamp"
    )

    process_name = (
        process_data["process_name"].iloc[0]
    )

    print(
        f"\nGenerating memory graph "
        f"for PID {pid}..."
    )

    plt.figure(figsize=(12, 6))

    plt.plot(
        process_data["timestamp"],
        process_data["memory_mb"],
        marker="o",
        markersize=3,
        linewidth=2
    )

    plt.xlabel("Time")

    plt.ylabel("Memory Usage (MB)")

    plt.title(
        f"Memory Usage Over Time - "
        f"{process_name} (PID {pid})"
    )

    plt.xticks(
        rotation=45
    )

    plt.grid(
        True,
        alpha=0.3
    )

    plt.tight_layout()

    output_file = (
        f"data/memory_graph_{pid}.png"
    )

    plt.savefig(
        output_file,
        dpi=150
    )

    print(
        f"Graph saved to: {output_file}"
    )

    plt.show()


if __name__ == "__main__":

    if len(sys.argv) != 2:

        print(
            "\nUsage:"
        )

        print(
            "python visualize.py <PID>"
        )

        print(
            "\nExample:"
        )

        print(
            "python visualize.py 6989"
        )

        sys.exit(1)

    pid = int(
        sys.argv[1]
    )

    visualize_process(pid)
