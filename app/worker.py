import os
import time

import redis

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")


def process_task(payload: str) -> dict[str, float | str]:
    started = time.perf_counter()
    value = float(payload)
    result = value
    for _ in range(500):
        result = (result * 1.000001 + 0.000001) % 1000003
    return {"input": value, "result": result, "elapsed": time.perf_counter() - started}


def main() -> None:
    client = redis.from_url(REDIS_URL, decode_responses=True)
    print("ScaleBench worker listening for tasks")
    while True:
        item = client.blpop("scs:tasks", timeout=5)
        if item is None:
            continue
        _, payload = item
        output = process_task(payload)
        client.rpush("scs:results", str(output))


if __name__ == "__main__":
    main()
