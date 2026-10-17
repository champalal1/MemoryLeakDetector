import pandas as pd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

FILE = "data/phase2_detector_results.csv"
OUTPUT = "data/phase2_risk_comparison.png"

df = pd.read_csv(FILE)
df["risk_score"] = pd.to_numeric(df["risk_score"], errors="coerce")
df = df.dropna(subset=["risk_score"])

if df.empty:
    print("No numeric risk scores found.")
    raise SystemExit(1)

print("\nPHASE 2 RISK SCORES")
for _, row in df.iterrows():
    print(
        f"{row['test_case']:<38} "
        f"{row['risk_score']:>6.2f}/100  "
        f"{row['result']}"
    )

plt.figure(figsize=(12, 6))
plt.bar(df["test_case"], df["risk_score"])
plt.axhline(30, linestyle="--", label="Normal / Low Risk boundary")
plt.axhline(50, linestyle="--", label="Low Risk / Suspicious boundary")
plt.xlabel("Test Scenario")
plt.ylabel("Risk Score (0–100)")
plt.title("Phase 2 Memory Leak Detector Risk Scores")
plt.xticks(rotation=25, ha="right")
plt.ylim(0, 100)
plt.legend()
plt.tight_layout()
plt.savefig(OUTPUT, dpi=150)
plt.close()

print(f"\nGraph saved to: {OUTPUT}")
