import json
import random
import time
import urllib.request

API = "http://localhost:8000/process"


def send_batch(size: int = 50) -> None:
    events = [
        {
            "device_id": f"edge-{i % 10}",
            "value": round(random.uniform(0, 100), 3),
            "timestamp": time.time(),
        }
        for i in range(size)
    ]
    request = urllib.request.Request(
        API,
        data=json.dumps({"events": events}).encode(),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        print(response.read().decode())


if __name__ == "__main__":
    for _ in range(5):
        send_batch()
        time.sleep(1)
