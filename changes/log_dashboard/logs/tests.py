from django.test import TestCase
from .models import AnomalyLog
from django.utils import timezone

class AnomalyLogModelTest(TestCase):
    def setUp(self):
        # Create a sample anomaly log entry
        self.log = AnomalyLog.objects.create(
            timestamp=timezone.now().timestamp(),
            level="ERROR",
            message="Test error log"
        )

    def test_anomaly_log_creation(self):
        # Test if the anomaly log is created successfully
        log = AnomalyLog.objects.first()
        self.assertIsNotNone(log)
        self.assertEqual(log.level, "ERROR")
        self.assertIn("Test error log", log.message)

    def test_str_representation(self):
        # Test the string representation of the anomaly log
        expected_str = f"[{self.log.level}] {self.log.message[:50]}"
        self.assertEqual(str(self.log), expected_str)
