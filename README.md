# 🧠 AI-Driven Real-Time Log Anomaly Detection Dashboard

🚀 This project is a full-stack, containerized platform that performs **real-time anomaly detection** on log streams using Kafka, a machine learning model, Prometheus, Grafana, and a Django REST API backend. Ideal for monitoring microservices and cloud-native systems.

---

## 🔧 Tech Stack

- **Python 3.12**
- **Apache Kafka** for real-time log streaming
- **Django** (REST API) for log/anomaly management
- **ML Model** (Isolation Forest) for anomaly detection
- **Prometheus** for monitoring metrics
- **Grafana** for data visualization
- **Docker** & **Docker Compose** for containerization
- **GitHub Actions** for CI/CD

---

## 📁 Project Structure

log_dashboard/
├── .github/workflows/django-ci.yml
├── log_dashboard/
├── logs/
│ ├── models.py
│ ├── views.py
│ ├── serializers.py
│ └── tests.py
log_anomaly_detector/
├── kafka/
│ ├── docker-compose.yml
│ └── Prometheus.yml
├── log-generator/
│ ├── producer.py
│ └── consumer_anomaly.py


---

## ⚙️ Run the Project

bash
Step 1: Start all containers
cd log_anomaly_detector/kafka
docker-compose up -d

Step 2: Start manage.py
cd log_dashboard
python manage.py runserver

Step 3: Start ML model
cd log_generator
python consumer_anomaly.py

Step 4: Start log producer
cd ../log-generator
python producer.py

Step 5: Open Prometheus at http://localhost:9090
Run queries like anomalies_detected_toal and log_anomaly_score

Step 6: Open Grafana at http://localhost:3000
See changes in real time and choose the kind of graph for Visual representation of the changes

Step 7: Open Django at http://localhost:8000
Django: Hit `http://localhost:8000/anomalies/` to check real time changes in anomalies

Step 8: Check .github/workflows/django-ci.yml for tests and linting on push.

## 🧠 Architecture Overview

text
[Log Generator] --> [Kafka Topic] --> [Kafka Consumer + ML Model] --> [Django API]
                                                               ↘
                                                          [Prometheus]
                                                               ↘
                                                          [Grafana]

## For Running tests
cd log_dashboard
python manage.py test logs
