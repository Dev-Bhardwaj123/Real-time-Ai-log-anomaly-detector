from django.urls import path
from . import views

urlpatterns = [
    path("anomalies/", views.get_anomalies, name="get_anomalies"),
    path("upload-log/", views.upload_log, name="upload_log"),
]
