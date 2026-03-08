from kafka import KafkaConsumer
import json
import pandas as pd
from sklearn.ensemble import IsolationForest
from prometheus_client import Counter, start_http_server, Gauge
import requests
import time  # ✅ Needed for delay handling
import logging

# 🔧 Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# 📊 Prometheus metrics
anomaly_counter = Counter('anomalies_detected_total', 'Total number of anomalies detected')
anomaly_score = Gauge("log_anomaly_score", "Anomaly score from ML model")

# 🚀 Start Prometheus metrics server
start_http_server(8001)  # Exposes metrics at http://localhost:8001/metrics

# 🔌 Kafka Consumer Setup
try:
    consumer = KafkaConsumer(
        'logs',
        bootstrap_servers='localhost:9092',
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        value_deserializer=lambda v: json.loads(v.decode('utf-8'))
    )
except Exception as e:
    logging.error("❌ Could not connect to Kafka broker at localhost:9092. Make sure Kafka is running.")
    raise e

# ⚙️ Buffer and model
log_buffer = []
BUFFER_SIZE = 100
model = IsolationForest(contamination=0.05, random_state=42)

def extract_features(logs):
    df = pd.DataFrame(logs)

    # ✅ Check and fill missing values to avoid errors
    df['level'] = df['level'].fillna('INFO')
    df['message'] = df['message'].fillna('')
    df['timestamp'] = pd.to_numeric(df['timestamp'], errors='coerce').fillna(0)

    df['level_num'] = df['level'].map({'INFO': 0, 'WARN': 1, 'ERROR': 2}).fillna(0)
    df['msg_len'] = df['message'].apply(len)
    df['time_diff'] = df['timestamp'] - df['timestamp'].min()

    return df[['level_num', 'msg_len', 'time_diff']]

print("✅ Starting consumer and anomaly detection...")

for message in consumer:
    log = message.value
    print("📝 Consumed log:", log)

    if {'timestamp', 'level', 'message'}.issubset(log):
        log_buffer.append(log)

    if len(log_buffer) == BUFFER_SIZE:
        try:
            features = extract_features(log_buffer)
            model.fit(features)
            preds = model.predict(features)

            anomalies = [log_buffer[i] for i in range(len(preds)) if preds[i] == -1]
            anomaly_count = len(anomalies)
            print(f"🚨 Detected {anomaly_count} anomalies in the batch")

            # 🔄 Update Prometheus
            anomaly_counter.inc(anomaly_count)
            anomaly_score.set(anomaly_count / BUFFER_SIZE)

            # 📤 Post anomalies to Django backend
            if anomalies:
                try:
                    res = requests.post("http://localhost:8000/api/upload-log/", json=anomalies)
                    print("✅ Posted anomalies to Django:", res.status_code)
                except Exception as e:
                    print("❌ Failed to post to Django:", e)

        except Exception as e:
            logging.error("❌ Error during anomaly detection or data processing:", exc_info=e)

        log_buffer = []
