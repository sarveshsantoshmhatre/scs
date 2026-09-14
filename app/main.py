import os
import time
from typing import Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from prometheus_client import Counter, Histogram, generate_latest
from starlette.responses import Response

REQUESTS = Counter("scs_requests_total", "Total API requests")
LATENCY = Histogram("scs_request_latency_seconds", "API request latency")

app = FastAPI(title="ScaleBench API", version="0.1.0")


class Event(BaseModel):
    device_id: str = Field(min_length=1)
    value: float
    timestamp: float | None = None


class Batch(BaseModel):
    events: list[Event] = Field(min_length=1, max_length=10000)


def _event_score(event: Event) -> float:
    # Deterministic CPU work so scaling experiments are reproducible.
    x = abs(event.value) + 1.0
    for _ in range(250):
        x = (x * 1.000001) % 1000003
    return x


@app.middleware("http")
async def metrics_middleware(request, call_next):
    started = time.perf_counter()
    REQUESTS.inc()
    response = await call_next(request)
    LATENCY.observe(time.perf_counter() - started)
    return response


@app.get("/")
def root() -> dict[str, Any]:
    return {"service": "ScaleBench", "status": "ok", "architecture": "client -> api -> workers -> storage"}


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "healthy"}


@app.post("/process")
def process(batch: Batch) -> dict[str, Any]:
    if not batch.events:
        raise HTTPException(400, "events cannot be empty")
    started = time.perf_counter()
    results = [_event_score(event) for event in batch.events]
    elapsed = time.perf_counter() - started
    return {
        "events": len(results),
        "elapsed_seconds": round(elapsed, 6),
        "throughput_events_per_second": round(len(results) / max(elapsed, 1e-9), 2),
        "checksum": round(sum(results), 4),
    }


@app.get("/metrics")
def metrics() -> Response:
    return Response(generate_latest(), media_type="text/plain; version=0.0.4")
