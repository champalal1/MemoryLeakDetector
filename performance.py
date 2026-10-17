import pandas as pd

FILE = "data/phase2_detector_results.csv"

def main():
    df = pd.read_csv(FILE)

    expected = {
        "Continuous Leak - Phase 2 Baseline": "LEAK",
        "Stable Memory": "NORMAL",
        "Gradual Leak": "LEAK",
        "Temporary Memory": "NORMAL",
        "Memory Intensive": "NORMAL",
    }

    detected_labels = {
        "SUSPICIOUS",
        "HIGH RISK",
        "POTENTIAL MEMORY LEAK",
        "POTENTIAL_LEAK",
    }
    df["expected"] = df["test_case"].map(expected)
    df["result_clean"] = df["result"].astype(str).str.strip().str.upper()
    df["detected_leak"] = df["result_clean"].isin(detected_labels)
    df["predicted"] = df["detected_leak"].map(
        {True: "LEAK", False: "NORMAL"}
    )

    known = df.dropna(subset=["expected"])
    correct = (known["expected"] == known["predicted"]).sum()
    accuracy = correct / len(known) * 100 if len(known) else 0

    normal = known[known["expected"] == "NORMAL"]
    leaks = known[known["expected"] == "LEAK"]

    false_positives = normal["detected_leak"].sum()
    false_positive_rate = (
        false_positives / len(normal) * 100 if len(normal) else 0
    )

    true_positives = leaks["detected_leak"].sum()
    detection_rate = (
        true_positives / len(leaks) * 100 if len(leaks) else 0
    )

    print("\n======================================")
    print(" PHASE 2 DETECTOR PERFORMANCE")
    print("======================================")
    print(f"Experiments evaluated: {len(known)}")
    print(f"Correct classifications: {correct}/{len(known)}")
    print(f"Binary classification accuracy: {accuracy:.2f}%")
    print(
        f"Leak detection rate: {detection_rate:.2f}% "
        f"({true_positives}/{len(leaks)})"
    )
    print(
        f"False-positive rate: {false_positive_rate:.2f}% "
        f"({false_positives}/{len(normal)})"
    )

    print("\nIndividual results:")
    for _, row in known.iterrows():
        print(
            f"{row['test_case']:<38} "
            f"Expected: {row['expected']:<6} "
            f"Predicted: {row['predicted']:<6} "
            f"Score: {row['risk_score']:.2f}"
        )

    print("\nNote: Metrics are preliminary and based on one run per scenario.")
    print("======================================\n")

if __name__ == "__main__":
    main()
