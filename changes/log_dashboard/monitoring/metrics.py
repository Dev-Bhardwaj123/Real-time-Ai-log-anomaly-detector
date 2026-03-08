from prometheus_client import Counter, Histogram

# Count how many anomalies detected
ANOMALY_COUNT = Counter('anomalies_detected_total', 'Total number of anomalies detected')

# Measure time taken for model prediction
PREDICTION_LATENCY = Histogram('model_prediction_latency_seconds', 'Time taken for anomaly detection model prediction')
