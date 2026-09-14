# Syllabus-to-Implementation Map

The academic syllabus has six modules. This document makes the mapping explicit so the repository can be used as both a learning project and a portfolio artifact.

## Module 1 — Introduction to Scalable Computing

Topics: need for scalability, large-scale systems, vertical/horizontal scaling, throughput, response time, multicore/GPU overview.

Implementation:
- `benchmarks/run_benchmark.py` measures throughput and elapsed time.
- Docker Compose provides a repeatable multi-service environment.
- The benchmark can be run with different worker counts to compare horizontal scaling.
- `docs/performance.md` records how to interpret the measurements.

## Module 2 — Parallel and Distributed Computing

Topics: task/data parallelism, distributed systems, client-server architecture, peer-to-peer systems.

Implementation:
- FastAPI is the client-server entry point.
- Redis-backed workers form a simple distributed task queue.
- Multiple worker containers represent parallel task execution.
- The project documentation explains task vs data parallelism.

## Module 3 — Cloud Computing Fundamentals

Topics: cloud deployment models, IaaS/PaaS/SaaS, virtualization, containers and Docker.

Implementation:
- `Dockerfile` packages the application.
- `compose.yaml` deploys the API, workers, Redis, and PostgreSQL as separate services.
- Documentation maps the local deployment to IaaS/PaaS/SaaS concepts.

## Module 4 — Data Management in Scalable Systems

Topics: distributed storage, replication, NoSQL, big data, Hadoop/Spark.

Implementation:
- PostgreSQL is the durable relational store.
- Redis is used for queueing/caching-style workloads.
- `data/` contains event-oriented input suitable for batch analytics.
- `docs/data-management.md` explains how the architecture could extend to Spark/Hadoop-scale pipelines.

## Module 5 — Performance and Scalability

Topics: scalability, metrics, benchmarking, Amdahl's Law, load balancing.

Implementation:
- Benchmarking script measures throughput and speedup.
- The project documents serial work and parallel work so Amdahl's Law can be applied.
- Worker queues provide a simple load-distribution mechanism.

## Module 6 — Emerging Trends and Applications

Topics: edge computing, IoT, serverless, green computing, cloud case studies.

Implementation:
- `edge/` simulates lightweight IoT event production close to the source.
- `serverless/` provides a function-style adapter around the processing logic.
- `docs/emerging-trends.md` connects the design to edge/serverless/energy-aware deployment decisions.

## Portfolio emphasis

The goal is not to claim production-grade distributed infrastructure. The goal is to demonstrate that a final-year B.Tech CSE student can translate core scalable-computing concepts into an observable, reproducible system and explain the trade-offs.