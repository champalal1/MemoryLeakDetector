# Memory Leak Detection and Prevention System

A Python-based system for monitoring process memory usage, detecting potential memory leaks using heuristic risk scoring, and providing prevention recommendations through an interactive Streamlit dashboard.

## Project Overview

Memory leaks can cause applications to consume increasing amounts of memory over time, potentially reducing system performance or causing instability.

This project monitors process memory usage, analyzes memory-growth patterns, assigns risk classifications, and provides alerts to help investigate suspicious behavior.

## Features

- **Process monitoring:** Collects process memory usage using `psutil`.
- **Risk analysis:** Evaluates memory growth, consistency, trend, duration, and growth rate.
- **Interactive dashboard:** Displays process metrics, risk classifications, and memory usage charts.
- **Automatic refresh:** Periodically refreshes dashboard data.
- **Risk alerts:** Highlights suspicious, high-risk, and potential memory-leak classifications.
- **Prevention safeguards:** Checks system and process memory thresholds and provides recommendations.
- **CSV exports:** Downloads risk summaries and memory measurements.
- **Experimental testing:** Includes controlled workloads for continuous leaks, gradual leaks, stable memory, temporary allocations, and memory-intensive behavior.
- **Performance evaluation:** Includes tools for analyzing detector performance and monitoring overhead.

## Technology Stack

- Python
- psutil
- NumPy
- pandas
- Streamlit
- Matplotlib and other visualization dependencies used by the project

## Project Structure

```text
MemoryLeakDetector/
├── main.py
├── monitor.py
├── detector.py
├── prevention.py
├── logger.py
├── dashboard.py
├── experiment_runner.py
├── performance.py
├── final_results.py
├── overhead_test.py
├── visualize.py
├── tests/
│   ├── memory_leak.py
│   ├── gradual_leak.py
│   ├── stable_memory.py
│   ├── temporary_memory.py
│   └── memory_intensive.py
├── data/
│   ├── memory_logs.csv
│   ├── experiment_results.csv
│   ├── phase2_detector_results.csv
│   └── archive/
├── reports/
│   └── phase2_validation_report.md
├── visualizations/
├── backup/
├── requirements.txt
└── README.md
```

## Installation

Clone the repository and enter the project directory:

```bash
git clone https://github.com/champalal1/MemoryLeakDetector.git
cd MemoryLeakDetector
```

Create and activate a virtual environment on Ubuntu or WSL:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the System

### 1. Start process monitoring

```bash
python main.py
```

The monitoring process records memory measurements in `data/memory_logs.csv`. Stop monitoring with `Ctrl+C`.

### 2. Start the dashboard

Open another terminal, activate the virtual environment, and run:

```bash
streamlit run dashboard.py
```

Open the local URL printed by Streamlit, normally `http://localhost:8501`.

Keep the monitoring process running to collect new measurements. The dashboard refreshes periodically and displays the latest data available in the log.

### 3. Run controlled experiments

Example:

```bash
python tests/stable_memory.py
python tests/memory_intensive.py
python tests/temporary_memory.py
python tests/gradual_leak.py
python tests/memory_leak.py
```

Some workloads run continuously. Stop them with `Ctrl+C` after an appropriate test interval, and avoid running multiple memory-intensive tests simultaneously.

## Risk Classification

The detector assigns heuristic risk scores from 0 to 100.

| Score | Classification |
|---:|---|
| 0–30 | NORMAL |
| Above 30–40 | LOW RISK |
| Above 40–60 | SUSPICIOUS |
| Above 60–80 | HIGH RISK |
| Above 80 | POTENTIAL MEMORY LEAK |

The classifications indicate patterns that deserve investigation; they do not prove that a process has a memory leak.

## Prevention Safeguards

The current safeguards include configurable system-memory and process-memory thresholds, alerts, and recommendations.

- Default system memory warning threshold: 85%.
- Default process RSS warning threshold: 500 MB.

These are configurable warning thresholds, not universal limits. High memory usage alone does not prove a leak. The current implementation provides recommendations and does not automatically terminate processes or repair application memory leaks.

## Experimental Evaluation

The project includes controlled workloads and recorded experiments for evaluating memory growth patterns, risk classification, and monitoring overhead.

Detailed validation notes and existing visualizations are stored in:

- `reports/phase2_validation_report.md`
- `visualizations/`

Results should be interpreted in the context of the tested workloads and environment. The existing experiments are preliminary and do not establish general performance across all applications.

## Limitations

- The detector uses heuristic scoring rather than definitive proof of a memory leak.
- Controlled test workloads do not represent every real-world application.
- Processes outside the monitoring selection may not be recorded.
- Prevention safeguards provide warnings and recommendations rather than automatic remediation.
- Detection accuracy and false-positive rates require further independent validation.

## Future Improvements

- Expand validation using more applications and workload types.
- Improve detection calibration and false-positive analysis.
- Add historical risk-score persistence and reporting.
- Add configurable alert thresholds and notification mechanisms.
- Explore safe, application-specific remediation strategies.

## Author

Developed as an operating systems project focused on memory monitoring, leak-risk detection, and prevention safeguards.
