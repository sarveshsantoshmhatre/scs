import argparse
import json
import statistics
import time
from concurrent.futures import ThreadPoolExecutor
from urllib.request import Request, urlopen


def call(url: str, events: int) -> tuple[float, int]:
    payload = {"events": [{"device_id": f"d{i%100}", "value": (i % 100) / 10.0} for i in range(events)]}
    body = json.dumps(payload).encode()
    request = Request(url, data=body, headers={"Content-Type": "application/json"})
    started = time.perf_counter()
    with urlopen(request, timeout=120) as response:
        response.read()
    return time.perf_counter() - started, events


def main() -> None:
    parser = argparse.ArgumentParser(description="ScaleBench throughput/latency benchmark")
    parser.add_argument("--workers", nargs="+", type=int, default=[1, 2, 4])
    parser.add_argument("--events", type=int, default=1000)
    parser.add_argument("--url", default="http://localhost:8000/process")
    args = parser.parse_args()

    baseline = None
    print("workers,events,elapsed_s,throughput_events_s,speedup")
    for workers in args.workers:
        samples = []
        with ThreadPoolExecutor(max_workers=workers) as pool:
            futures = [pool.submit(call, args.url, args.events) for _ in range(workers)]
            for future in futures:
                samples.append(future.result())
        elapsed = sum(item[0] for item in samples)
        total_events = sum(item[1] for item in samples)
        throughput = total_events / max(elapsed, 1e-9)
        baseline = baseline or throughput
        speedup = throughput / baseline
        print(f"{workers},{total_events},{statistics.mean(x[0] for x in samples):.4f},{throughput:.2f},{speedup:.2f}")


if __name__ == "__main__":
    main()
