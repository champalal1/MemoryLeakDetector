# Phase 2: Memory Leak Detector Validation Report

## 1. Objective
Evaluate the detector using controlled memory workloads and measure
the monitoring process's CPU and memory overhead.

## 2. Controlled Experiments

| Scenario | PID | Risk Score | Classification |
|---|---:|---:|---|
| Stable memory-intensive workload | 669 | 20.95 | NORMAL |
| Continuous memory leak | 777 | 86.96 | POTENTIAL MEMORY LEAK |
| Temporary memory allocation | 848 | 18.55 | NORMAL |
| Gradual memory leak, run 1 | 928 | 48.47 | SUSPICIOUS |
| Gradual memory leak, run 2 | 1015 | 48.48 | SUSPICIOUS |
| Continuous memory leak | 1207 | 93.24 | POTENTIAL MEMORY LEAK |

## 3. Monitoring Overhead

- Measurements: 30
- Average CPU usage: 0.53%
- Peak CPU usage: 2.00%
- Average RSS memory: 13.90 MB
- Peak RSS memory: 13.91 MB

These measurements describe one test environment and one measurement run.

## 4. Estimated Threshold-Crossing Times

For continuous leak PID 1207, offline analysis of progressively
longer data prefixes reported:

- SUSPICIOUS: approximately 1.0 second
- HIGH RISK: approximately 10.1 seconds
- POTENTIAL MEMORY LEAK: approximately 35.2 seconds

These are offline threshold-crossing estimates, not measured live alert
latencies. The scoring implementation was checked against detector.py.

## 5. Findings

- Stable memory usage was classified as NORMAL.
- Continuous memory growth was classified as POTENTIAL MEMORY LEAK.
- Temporary memory allocation was classified as NORMAL.
- Gradual memory growth was classified as SUSPICIOUS in two similar runs.
- The repeated gradual-leak scores differed by only 0.01 points.
- Monitoring overhead appeared low during the measured run.

## 6. Limitations

- Experiments used controlled Python test scripts, not production services.
- The number and variety of experiments are limited.
- Thresholds require evaluation on independent workloads.
- Threshold-crossing times were estimated offline.
- Automatic real-time alerting and memory-leak prevention have not
  been validated by these experiments.

## 7. Next Steps

1. Repeat scenarios across multiple runs.
2. Test additional application workloads.
3. Evaluate false positives and missed leaks on independent test cases.
4. Measure monitoring overhead under heavier system load.
5. Implement and validate live alerts if required.
6. Build a dashboard after the detector's behavior is validated.
