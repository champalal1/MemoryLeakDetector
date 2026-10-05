import pandas as pd
import matplotlib.pyplot as plt


FILE = "data/experiment_results.csv"

df = pd.read_csv(FILE)

print("\n======================================")
print("       FINAL EXPERIMENT ANALYSIS")
print("======================================")

print("\nTest Results:\n")

for _, row in df.iterrows():

    print(
        f"{row['test_case']:<20} "
        f"Risk Score: "
        f"{row['leak_score']:.2f} "
        f"Result: "
        f"{row['result']}"
    )


# Create risk score graph

plt.figure(figsize=(12, 6))

plt.bar(
    df["test_case"],
    df["leak_score"]
)

plt.xlabel("Test Case")
plt.ylabel("Leak Risk Score")
plt.title("Memory Leak Detection Results")

plt.xticks(
    rotation=25,
    ha="right"
)

plt.ylim(0, 100)

plt.tight_layout()

output = "data/final_risk_comparison.png"

plt.savefig(
    output,
    dpi=150
)

print(
    f"\nGraph saved to: {output}"
)

plt.show()
