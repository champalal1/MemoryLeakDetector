# Memory Leak Detection and Prevention System

## Overview

The Memory Leak Detection and Prevention System is an Operating Systems project designed to monitor process memory usage, analyze memory growth patterns, and identify potential memory leaks.

The system continuously collects process-level memory information and stores the observations in a CSV log. The collected data is analyzed using memory growth, growth rate, trend analysis, and a weighted leak risk score.

The system classifies processes into categories such as:

- NORMAL
- SUSPICIOUS
- HIGH RISK / POTENTIAL LEAK

## Objectives

### Phase 1

- Study existing memory leak detection techniques.
- Monitor process-level memory usage.
- Define memory usage and leak detection metrics.
- Design and implement a prototype memory leak detection system.

### Phase 2

- Test the system using memory-intensive applications.
- Detect and analyze memory growth under different scenarios.
- Optimize the detection algorithm.
- Evaluate detection accuracy and false-positive rate.
- Measure CPU and memory overhead.
- Validate the system using a memory-intensive workload.

## System Architecture

The system consists of the following modules:

1. Process Monitor
2. Memory Logger
3. Memory Data Storage
4. Leak Analyzer
5. Risk Score Calculator
6. Visualization Module
7. Experiment and Performance Analysis Module

## Detection Metrics

The system evaluates memory behavior using:

- Initial memory usage
- Final memory usage
- Total memory growth
- Memory growth rate
- Memory trend slope
- Growth consistency
- Monitoring duration
- Leak risk score

## Risk Classification

The prototype uses a 0–100 leak risk score.

The score is used to identify:

- NORMAL memory behavior
- SUSPICIOUS memory growth
- HIGH RISK / POTENTIAL MEMORY LEAK

## Experimental Evaluation

The system was evaluated using five controlled scenarios:

| Test Case | Result |
|---|---|
| Stable Memory | NORMAL |
| Continuous Leak | HIGH RISK |
| Gradual Leak | SUSPICIOUS |
| Temporary Memory | NORMAL |
| Memory Intensive | NORMAL |

### Measured Results

- Controlled test classifications: 5/5
- Detection accuracy: 100%
- False-positive rate: 0%
- Leak detection rate: 100%
- Average CPU usage: 0.68%
- Maximum CPU usage: 7.00%
- Average RAM usage: 13.89 MB
- Maximum RAM usage: 13.90 MB

The accuracy values above apply to the five controlled experimental scenarios evaluated during this project and should not be interpreted as universal real-world accuracy.

## Project Structure

```text
MemoryLeakDetector/
│
├── main.py
├── monitor.py
├── logger.py
├── detector.py
├── visualize.py
├── experiment_runner.py
├── performance.py
├── final_results.py
├── overhead_test.py
│
├── tests/
│   ├── temporary_memory.py
│   └── memory_intensive.py
│
├── data/
│   ├── memory_logs.csv
│   ├── experiment_results.csv
│   ├── memory graphs
│   └── final_risk_comparison.png
│
├── requirements.txt
└── README.md
