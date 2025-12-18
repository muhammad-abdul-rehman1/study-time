from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime

class StudySession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='study_sessions')
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(null=True, blank=True)

    @property
    def duration(self):
        if self.end_time:
            return self.end_time - self.start_time
        return timezone.now() - self.start_time

    @property
    def is_active(self):
        return self.end_time is None

    def __str__(self):
        return f"{self.user.username} - {self.start_time.date()}"
