# Emerging Trends

Module 6 covers edge computing, IoT applications, serverless computing, green computing, and cloud-based case studies. fileciteturn0file0L121-L125

## Edge + IoT

`edge/simulator.py` generates device events locally and sends them in batches. In a real deployment, an edge node could pre-aggregate or filter data before sending only useful events to the cloud.

## Serverless

`serverless/handler.py` exposes the processing logic as a function-style handler so the same computation can be mapped to a Function-as-a-Service platform.

## Green computing

The benchmark should be used to discuss the performance/energy trade-off: using more workers can reduce completion time but may increase instantaneous resource consumption. A useful future experiment is energy per processed event under different worker counts.
