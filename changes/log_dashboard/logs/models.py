from django.db import models

class AnomalyLog(models.Model):
    timestamp = models.FloatField()
    level = models.CharField(max_length=10)
    message = models.TextField()
    detected_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.level}] {self.message[:50]}"

