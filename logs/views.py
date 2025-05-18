from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import AnomalyLog
from .serializers import AnomalyLogSerializer
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from django.http import HttpResponse

# Define metrics
log_counter = Counter('logs_processed_total', 'Total number of logs processed')
anomaly_counter = Counter('anomalies_detected_total', 'Total number of anomalies detected')

def metrics_view(request):
    return HttpResponse(generate_latest(), content_type=CONTENT_TYPE_LATEST)

@api_view(["GET"])
def get_anomalies(request):
    logs = AnomalyLog.objects.all().order_by('-detected_at')[:100]  # limit to 100
    serializer = AnomalyLogSerializer(logs, many=True)
    return Response(serializer.data)

@api_view(["POST"])
def upload_log(request):
    serializer = AnomalyLogSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
