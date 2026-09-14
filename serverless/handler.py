def handler(event, context=None):
    events = event.get("events", [])
    checksum = 0.0
    for item in events:
        x = abs(float(item.get("value", 0))) + 1.0
        for _ in range(100):
            x = (x * 1.000001) % 1000003
        checksum += x
    return {
        "statusCode": 200,
        "body": {"events": len(events), "checksum": checksum},
    }
