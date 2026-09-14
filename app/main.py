import os
import time
from concurrent.futures import ThreadPoolExecutor
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from prometheus_client import Counter, Histogram, generate_latest
from starlette.responses import Response

REQUESTS = Counter("scs_requests_total", "Total API requests")
LATENCY = Histogram("scs_request_latency_seconds", "API request latency")

WORKERS = max(1, int(os.getenv("WORKERS", "2")))
executor = ThreadPoolExecutor(max_workers=WORKERS)

app = FastAPI(title="ScaleBench", version="1.0.0")


class Event(BaseModel):
    device_id: str = Field(min_length=1)
    value: float
    timestamp: float | None = None


class Batch(BaseModel):
    events: list[Event] = Field(min_length=1, max_length=10000)


def _event_score(event: Event) -> float:
    x = abs(event.value) + 1.0
    for _ in range(250):
        x = (x * 1.000001) % 1000003
    return x


def _process(batch: Batch) -> dict[str, Any]:
    started = time.perf_counter()
    futures = [executor.submit(_event_score, event) for event in batch.events]
    results = [future.result() for future in futures]
    elapsed = time.perf_counter() - started
    return {
        "events": len(results),
        "elapsed_seconds": round(elapsed, 6),
        "throughput_events_per_second": round(len(results) / max(elapsed, 1e-9), 2),
        "checksum": round(sum(results), 4),
        "workers": WORKERS,
    }


@app.middleware("http")
async def metrics_middleware(request, call_next):
    started = time.perf_counter()
    REQUESTS.inc()
    response = await call_next(request)
    LATENCY.observe(time.perf_counter() - started)
    return response


@app.get("/", response_class=HTMLResponse)
@app.head("/")
def root() -> HTMLResponse:
    with open("app/index.html", "r", encoding="utf-8") as file:
        return HTMLResponse(file.read())


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "healthy"}


@app.get("/api/status")
def status() -> dict[str, Any]:
    return {"service": "ScaleBench", "status": "online", "workers": WORKERS, "architecture": "client -> api -> worker pool -> storage"}


@app.post("/process")
def process(batch: Batch) -> dict[str, Any]:
    if not batch.events:
        raise HTTPException(400, "events cannot be empty")
    return _process(batch)


@app.get("/metrics")
def metrics() -> Response:
    return Response(generate_latest(), media_type="text/plain; version=0.0.4")
