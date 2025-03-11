# Computer Networks Assignment: 2

## Overview
This repository contains Mininet-based network simulations to analyze different TCP congestion control schemes and TCP behavior with various configurations.

## Tasks

### Task 1: Comparison of Congestion Control Protocols
This task compares different TCP congestion control protocols using Mininet and iPerf3. The following congestion control schemes are analyzed:
- YeAH
- BBR
- Westwood

#### How to Run
```bash
python3 task1.py <option> <congestion_control_scheme>
```
- `<option>`: Choose from `a`, `b`, `c`, or `d` for different network conditions.
- `<congestion_control_scheme>`: Choose one of `yeah`, `bbr`, or `westwood`.

#### Output
- `iperf_capture.pcap`: Captured traffic file for analysis.
- `{host}_{cc_scheme}.txt`: iPerf logs for each host and congestion control scheme.

#### Metrics Analyzed
- Throughput
- Goodput
- Packet loss rate
- Maximum packet size achieved

### Task 2
The jupyter files in the repository were used for Task 2. The q2_part{1,2}.pcap show the network flow for corresponding parts.

### Task 3: TCP Performance Analysis with Nagle’s Algorithm and Delayed ACK
This task examines the impact of Nagle’s Algorithm and Delayed ACK on TCP performance by transmitting a 4 KB file at a fixed rate.

#### How to Run
```bash
python3 task3.py <nagle: 0|1> <delayed_ack: 0|1>
```
- `nagle`: `0` (disabled) or `1` (enabled)
- `delayed_ack`: `0` (disabled) or `1` (enabled)

#### Output
- `tcp_test.pcap`: Captured traffic file for analysis.
- Metrics such as throughput, goodput, packet loss rate, and max packet size.

#### Metrics Analyzed
- Throughput
- Goodput
- Packet loss rate
- Maximum packet size achieved

## Cleanup
To clean up any previous Mininet instances before running a new test:
```bash
sudo mn -c
```

