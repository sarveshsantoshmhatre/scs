# Performance Study

## Metrics

The project focuses on the same basic performance ideas emphasized in the syllabus: throughput and response time. fileciteturn0file0L89-L91

Run:

```bash
python -m benchmarks.run_benchmark --workers 1 2 4 8 --events 1000
```

Record for each worker count:

- total events processed
- elapsed time
- throughput (events/second)
- response/latency behavior
- observed speedup

## Amdahl's Law

For a parallel fraction `P` and `N` workers:

```text
Speedup(N) = 1 / ((1 - P) + P/N)
```

Use the measured single-worker and multi-worker throughput to compare observed speedup with the theoretical upper bound. This makes the scalability limit visible rather than treating more workers as automatically equivalent to more performance.

## What to discuss in a viva/interview

1. Why does throughput eventually stop scaling?
2. What part of the system remains serial?
3. How does queue contention affect latency?
4. When is vertical scaling preferable to horizontal scaling?
5. How would replication improve availability but increase coordination/storage cost?
6. How would the design change for millions of events per second?

The syllabus explicitly includes benchmarking, Amdahl's Law, and load-balancing fundamentals in Module 5. fileciteturn0file0L116-L119