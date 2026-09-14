# Scalable Systems Lab

A final-year B.Tech CSE capstone demonstrating the core concepts from **CE 403 – Scalable Computing and Systems** through one runnable system.

## Project
**ScaleBench: Fault-Tolerant Distributed Analytics Platform**

ScaleBench is a small but practical distributed application that ingests event data, processes it in parallel, stores replicated records, exposes a scalable API, and measures how the system behaves as workload and worker count change.

## Syllabus coverage

| Syllabus module | Implementation in this project |
|---|---|
| 1. Introduction to Scalable Computing | Throughput/latency measurement, vertical vs horizontal scaling experiment, CPU-bound workload comparison |
| 2. Parallel & Distributed Computing | Task parallelism, worker pool, client-server API, distributed worker architecture |
| 3. Cloud Computing Fundamentals | Docker containers, service separation, deployment-ready configuration, IaaS/PaaS/SaaS discussion |
| 4. Data Management | PostgreSQL, Redis cache, replicated worker results, batch analytics pipeline, Spark-compatible data layout |
| 5. Performance & Scalability | Benchmark scripts, latency percentiles, throughput, Amdahl's Law experiment, load balancing |
| 6. Emerging Trends & Applications | Edge-style ingestion service, IoT event simulation, serverless adapter example, energy/performance notes |

## Architecture

```text
                +------------------+
IoT / Client -> | FastAPI Gateway  |
                +--------+---------+
                         |
                   +-----v-----+
                   | Redis Queue|
                   +-----+-----+
                         |
             +-----------+-----------+
             |           |           |
          +--v--+     +--v--+     +--v--+
          |Worker|     |Worker|     |Worker|
          +--+--+     +--+--+     +--+--+
             |           |           |
             +-----------+-----------+
                         |
                  +------v------+
                  | PostgreSQL  |
                  +------+------+ 
                         |
                  +------v------+
                  | Analytics / |
                  | Benchmark   |
                  +-------------+
```

## Repository layout

```text
app/
  api/              FastAPI gateway and health endpoints
  workers/          parallel task workers and load balancing
  storage/          PostgreSQL/Redis adapters
  analytics/        aggregation and benchmark helpers
benchmarks/         reproducible scalability tests
data/               sample IoT/event data
edge/               lightweight edge-ingestion simulation
serverless/         serverless-compatible function adapter
docs/               architecture, syllabus mapping, experiments
scripts/             setup and benchmark commands
compose.yaml        multi-container local deployment
Dockerfile          application container
requirements.txt    Python dependencies
tests/              unit/integration tests
```

## Run locally

```bash
cp .env.example .env
docker compose up --build
```

Then open:

- API: `http://localhost:8000`
- Swagger UI: `http://localhost:8000/docs`
- Metrics: `http://localhost:8000/metrics`

## Benchmark

Run the baseline test:

```bash
python -m benchmarks.run_benchmark --workers 1 --events 10000
```

Compare horizontal scaling:

```bash
python -m benchmarks.run_benchmark --workers 1 2 4 8 --events 10000
```

The benchmark reports throughput, average latency, p95 latency, CPU time, and speedup. The report also estimates the serial fraction and compares the observed result with **Amdahl's Law**.

## Learning outcomes demonstrated

The project is intentionally designed as a portfolio-quality practical implementation rather than a collection of isolated examples. It demonstrates scalable-system reasoning, parallel/distributed models, cloud/container concepts, data management, performance analysis, and emerging architectures in one coherent system.

## Academic scope

This repository is aligned with the provided **CE 403 Scalable Computing and Systems** syllabus for AY 2023-24. The syllabus specifies six modules covering scalable computing, parallel/distributed systems, cloud fundamentals, scalable data management, performance/scalability, and emerging applications. fileciteturn0file0L82-L125
