from kafka import KafkaProducer
import json
import time
import random

# Connect to Kafka running on localhost:9092
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')  # Serialize Python dict to JSON bytes
)

levels = ["INFO", "WARN", "ERROR"]
messages = [
    "User logged in",
    "DB connection failed",
    "Cache cleared",
    "Payment initiated",
    "High memory usage",
    "Null pointer exception",
    "Disk I/O warning",
    "Unhandled exception",
    "User session expired",
    "Rate limit hit"
]

burst_interval = 30       # every 30 logs, simulate a burst
burst_duration = 5        # number of logs to simulate in burst mode
log_counter = 0

while True:
    # Burst mode simulation
    if log_counter % burst_interval < burst_duration:
        weights = [30, 40, 30]  # More WARN/ERROR logs
    else:
        weights = [80, 15, 5]   # Mostly INFO

    log = {
        "timestamp": time.time(),
        "level": random.choices(levels, weights=weights)[0],
        "message": random.choice(messages)
    }

    print("Produced log:", log)
    producer.send("logs", value=log)
    log_counter += 1
    time.sleep(random.uniform(0.5, 1.5))  # Vary timing to simulate realistic load
