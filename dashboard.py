from pathlib import Path
from streamlit_autorefresh import st_autorefresh
from prevention import (
    check_system_memory,
    get_prevention_recommendations,
)
import numpy as np
import pandas as pd
import streamlit as st

from detector import (
    calculate_growth_score,
    calculate_consistency_score,
    calculate_trend_score,
    calculate_duration_score,
    calculate_rate_score,
)

LOG_FILE = Path("data/memory_logs.csv")

st.set_page_config(
    page_title="Memory Leak Detector",
    page_icon="🛡️",
    layout="wide",
)
st_autorefresh(interval=5000, key="dashboard_refresh")

st.title("🛡️ Memory Leak Detection Dashboard")

st.divider()
st.subheader("🛡️ Prevention Safeguards")

system_check = check_system_memory(threshold=85)

st.metric(
    "System Memory Usage",
    f"{system_check['memory_percent']:.1f}%",
    delta=f"Alert threshold: {system_check['threshold']}%",
)

if system_check["alert"]:
    st.warning(system_check["message"])
else:
    st.success(system_check["message"])

st.write("**Recommendations**")
for recommendation in get_prevention_recommendations(
    system_check["alert"], False
):
    st.write(f"- {recommendation}")

st.caption("Process memory monitoring and leak-risk analysis")

st.sidebar.header("Settings")

window_minutes = st.sidebar.selectbox(
    "History window",
    [1, 5, 15, 60, 240, 1440],
    index=2,
    format_func=lambda x: (
        f"{x} minutes" if x < 60
        else f"{x // 60} hours" if x < 1440
        else "24 hours"
    ),
)

if st.sidebar.button("Refresh dashboard"):
    st.rerun()

if not LOG_FILE.exists():
    st.warning(f"Log file not found: {LOG_FILE}")
    st.info("Start monitoring with `python main.py`.")
    st.stop()

try:
    df = pd.read_csv(LOG_FILE)

    required = {
        "timestamp",
        "pid",
        "process_name",
        "memory_mb",
    }

    if not required.issubset(df.columns):
        st.error(
            "CSV is missing required columns: "
            + ", ".join(sorted(required - set(df.columns)))
        )
        st.stop()

    df["timestamp"] = pd.to_datetime(
        df["timestamp"], errors="coerce"
    )
    df["pid"] = pd.to_numeric(df["pid"], errors="coerce")
    df["memory_mb"] = pd.to_numeric(
        df["memory_mb"], errors="coerce"
    )

    df = df.dropna(
        subset=[
            "timestamp",
            "pid",
            "memory_mb",
            "process_name",
        ]
    )

    df["pid"] = df["pid"].astype(int)

except (OSError, pd.errors.ParserError, ValueError) as exc:
    st.error(f"Unable to read monitoring log: {exc}")
    st.stop()

if df.empty:
    st.warning("No valid measurements have been recorded yet.")
    st.info("Start monitoring with `python main.py`.")
    st.stop()

latest_time = df["timestamp"].max()

recent = df[
    df["timestamp"]
    >= latest_time - pd.Timedelta(minutes=window_minutes)
].copy()


def analyze(group):
    group = group.sort_values("timestamp")

    memory = group["memory_mb"].to_numpy(dtype=float)
    elapsed = (
        group["timestamp"] - group["timestamp"].iloc[0]
    ).dt.total_seconds().to_numpy()

    duration = float(elapsed[-1])

    if len(group) < 2 or duration <= 0:
        return None

    growth = float(memory[-1] - memory[0])
    rate = growth / duration
    slope = float(np.polyfit(elapsed, memory, 1)[0])

    score = min(
        calculate_growth_score(growth)
        + calculate_consistency_score(memory)
        + calculate_trend_score(slope)
        + calculate_duration_score(duration)
        + calculate_rate_score(rate),
        100,
    )

    if score <= 30:
        classification = "NORMAL"
    elif score <= 40:
        classification = "LOW RISK"
    elif score <= 60:
        classification = "SUSPICIOUS"
    elif score <= 80:
        classification = "HIGH RISK"
    else:
        classification = "POTENTIAL MEMORY LEAK"

    return {
        "PID": int(group["pid"].iloc[0]),
        "Process": str(group["process_name"].iloc[-1]),
        "Current RSS (MB)": round(float(memory[-1]), 2),
        "Growth (MB)": round(growth, 2),
        "Growth (MB/sec)": round(rate, 4),
        "Duration (sec)": round(duration, 2),
        "Samples": len(group),
        "Risk Score": round(score, 2),
        "Classification": classification,
    }


results = []

for _, group in recent.groupby("pid"):
    result = analyze(group)
    if result is not None:
        results.append(result)

if not results:
    st.warning(
        "Not enough measurements in this history window. "
        "Choose a longer window or collect more samples."
    )
    st.dataframe(recent.tail(50), use_container_width=True)
    st.stop()

summary = pd.DataFrame(results).sort_values(
    "Risk Score", ascending=False
)

total_processes = len(summary)
high_risk = int(
    summary["Classification"].isin(
        ["HIGH RISK", "POTENTIAL MEMORY LEAK"]
    ).sum()
)
potential_leaks = int(
    (summary["Classification"] == "POTENTIAL MEMORY LEAK").sum()
)
total_memory = float(
    recent.sort_values("timestamp")
    .groupby("pid")["memory_mb"]
    .last()
    .sum()
)

a, b, c, d = st.columns(4)

a.metric("Processes analyzed", total_processes)
b.metric("High-risk processes", high_risk)
c.metric("Potential leaks", potential_leaks)
d.metric("Latest recorded RSS", f"{total_memory:.2f} MB")

st.divider()

st.divider()
st.subheader("🔎 Process-Level Safeguards")

# Processes with high risk scores
risky_processes = summary[
    summary["Classification"].isin(
        ["HIGH RISK", "POTENTIAL MEMORY LEAK"]
    )
]

# Processes exceeding the configurable RSS threshold
process_memory_limit_mb = 500

memory_limit_processes = summary[
    summary["Current RSS (MB)"] >= process_memory_limit_mb
]

if not risky_processes.empty:
    st.warning(
        f"{len(risky_processes)} process(es) have high leak-risk scores."
    )

    for _, process in risky_processes.iterrows():
        st.write(
            f"**{process['Process']}** (PID {process['PID']}) — "
            f"Risk: {process['Risk Score']}/100, "
            f"RSS: {process['Current RSS (MB)']:.2f} MB"
        )

        st.caption(
            "Recommendation: inspect memory growth over time, "
            "review application logs, and investigate possible leaks."
        )
else:
    st.success("No high-risk process classifications in this history window.")

if not memory_limit_processes.empty:
    st.warning(
        f"{len(memory_limit_processes)} process(es) exceed "
        f"the {process_memory_limit_mb} MB RSS threshold."
    )

    for _, process in memory_limit_processes.iterrows():
        st.write(
            f"**{process['Process']}** (PID {process['PID']}) — "
            f"{process['Current RSS (MB)']:.2f} MB"
        )
else:
    st.info(
        f"No process exceeds the {process_memory_limit_mb} MB RSS threshold."
    )

st.subheader("Process Risk Overview")

st.subheader("🚨 Memory Leak Alerts")

critical = summary[
    summary["Classification"] == "POTENTIAL MEMORY LEAK"
]

high = summary[
    summary["Classification"] == "HIGH RISK"
]

suspicious = summary[
    summary["Classification"] == "SUSPICIOUS"
]

if not critical.empty:
    st.error(
        f"🚨 CRITICAL: {len(critical)} process(es) "
        "classified as potential memory leaks."
    )

    for _, process in critical.iterrows():
        st.write(
            f"**Process:** {process['Process']} | "
            f"**PID:** {process['PID']} | "
            f"**Risk Score:** {process['Risk Score']}/100"
        )

if not high.empty:
    st.warning(
        f"⚠️ HIGH RISK: {len(high)} process(es) need investigation."
    )

    for _, process in high.iterrows():
        st.write(
            f"**Process:** {process['Process']} | "
            f"**PID:** {process['PID']} | "
            f"**Risk Score:** {process['Risk Score']}/100"
        )

if not suspicious.empty:
    st.info(
        f"🔎 {len(suspicious)} process(es) classified as suspicious. "
        "Continue monitoring their memory trends."
    )

if critical.empty and high.empty and suspicious.empty:
    st.success("✅ No suspicious or high-risk processes detected.")

def color_risk(row):
    classification = row["Classification"]

    if classification == "POTENTIAL MEMORY LEAK":
        background = "#ffd6d6"
    elif classification == "HIGH RISK":
        background = "#ffe5c2"
    elif classification == "SUSPICIOUS":
        background = "#fff3bf"
    else:
        background = "#d9f7df"

    return [
        f"background-color: {background}; color: #000000;"
    ] * len(row)

st.dataframe(
    summary.style
    .apply(color_risk, axis=1)
    .set_properties(**{"color": "#000000"}),
    use_container_width=True,
    hide_index=True,
)

st.divider()

st.divider()
st.subheader("📈 Risk Score History")

risk_pid_options = summary["PID"].tolist()

risk_pid = st.selectbox(
    "Select process for risk history",
    risk_pid_options,
    key="risk_history_pid",
    format_func=lambda pid: (
        f"{pid} — "
        f"{summary.loc[summary['PID'] == pid, 'Process'].iloc[0]}"
    ),
)

risk_history = recent[recent["pid"] == risk_pid].copy()
risk_history = risk_history.sort_values("timestamp")

risk_points = []

# Calculate the risk score at successive prefixes of the process history.
# Require at least 2 samples and positive elapsed time.
for end in range(2, len(risk_history) + 1):
    group = risk_history.iloc[:end]
    result = analyze(group)

    if result is not None:
        risk_points.append({
            "Time": group["timestamp"].iloc[-1],
            "Risk Score": result["Risk Score"],
        })

if risk_points:
    risk_df = pd.DataFrame(risk_points).set_index("Time")

    st.line_chart(
        risk_df,
        height=300,
        x_label="Time",
        y_label="Risk Score (0–100)",
    )
    
    latest_score = risk_points[-1]["Risk Score"]
    st.metric("Latest calculated risk score", f"{latest_score:.2f}/100")
else:
    st.info(
        "Not enough distinct timestamps to calculate a risk history. "
        "Collect more measurements and refresh."
    )

st.subheader("Memory Usage History")

pid_options = summary["PID"].tolist()

selected_pid = st.selectbox(
    "Select process PID",
    pid_options,
    format_func=lambda pid: (
        f"{pid} — "
        f"{summary.loc[summary['PID'] == pid, 'Process'].iloc[0]}"
    ),
)

process_history = recent[
    recent["pid"] == selected_pid
].sort_values("timestamp")

if not process_history.empty:
    st.line_chart(
        process_history.set_index("timestamp")["memory_mb"],
        height=350,
        x_label="Time",
        y_label="Memory RSS (MB)",
    )

    selected_result = summary[
        summary["PID"] == selected_pid
    ].iloc[0]

    st.write(
        f"**Classification:** {selected_result['Classification']} "
        f"— Risk score: {selected_result['Risk Score']}/100"
    )

st.divider()

st.subheader("Recent Memory Measurements")

st.divider()
st.subheader("📥 Export Analysis Report")

report_csv = summary.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Risk Analysis (CSV)",
    data=report_csv,
    file_name="memory_leak_analysis.csv",
    mime="text/csv",
)

measurements_csv = recent.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Memory Measurements (CSV)",
    data=measurements_csv,
    file_name="memory_measurements.csv",
    mime="text/csv",
)

st.dataframe(
    recent.sort_values("timestamp", ascending=False).head(100),
    use_container_width=True,
    hide_index=True,
)

st.caption(
    "This dashboard analyzes recorded RSS measurements. "
    "Risk classifications are heuristic indicators, not proof of a memory leak. "
    "Click Refresh dashboard to reload the latest log data."
)
