import pandas as pd


FILE = "data/experiment_results.csv"


def main():

    df = pd.read_csv(FILE)

    print("\n======================================")
    print("       SYSTEM PERFORMANCE")
    print("======================================")

    print(
        f"\nTotal experiments : {len(df)}"
    )

    # Expected behavior
    expected = {
        "Stable Memory": "NORMAL",
        "Continuous Leak": "HIGH_RISK",
        "Gradual Leak": "SUSPICIOUS",
        "Temporary Memory": "NORMAL",
        "Memory Intensive": "NORMAL"
    }

    correct = 0

    for _, row in df.iterrows():

        test = row["test_case"]
        actual = row["result"]

        expected_result = expected.get(
            test
        )

        if actual == expected_result:
            correct += 1

    accuracy = (
        correct / len(df)
    ) * 100

    print(
        f"Correct classifications: "
        f"{correct}/{len(df)}"
    )

    print(
        f"Detection accuracy: "
        f"{accuracy:.2f}%"
    )

    # False positives
    normal_tests = df[
        df["test_case"].isin([
            "Stable Memory",
            "Temporary Memory",
            "Memory Intensive"
        ])
    ]

    false_positives = normal_tests[
        normal_tests["result"] != "NORMAL"
    ]

    if len(normal_tests) > 0:

        false_positive_rate = (
            len(false_positives) /
            len(normal_tests)
        ) * 100

    else:

        false_positive_rate = 0

    print(
        f"False positive rate: "
        f"{false_positive_rate:.2f}%"
    )

    # Leak detection
    leak_tests = df[
        df["test_case"].isin([
            "Continuous Leak",
            "Gradual Leak"
        ])
    ]

    detected = leak_tests[
        leak_tests["result"].isin([
            "POTENTIAL_LEAK",
            "HIGH_RISK",
            "SUSPICIOUS"
        ])
    ]

    if len(leak_tests) > 0:

        detection_rate = (
            len(detected) /
            len(leak_tests)
        ) * 100

    else:

        detection_rate = 0

    print(
        f"Leak detection rate: "
        f"{detection_rate:.2f}%"
    )

    # Average duration
    avg_duration = df[
        "duration_sec"
    ].mean()

    print(
        f"Average experiment duration: "
        f"{avg_duration:.2f} sec"
    )

    # Memory growth
    avg_growth = df[
        "total_growth_mb"
    ].mean()

    print(
        f"Average memory growth: "
        f"{avg_growth:.2f} MB"
    )

    print("\n======================================")
    print("             TEST SUMMARY")
    print("======================================")

    for _, row in df.iterrows():

        print(
            f"{row['test_case']:<20} "
            f"{row['result']:<12} "
            f"Score: "
            f"{row['leak_score']:.2f}"
        )

    print("======================================\n")


if __name__ == "__main__":
    main()
