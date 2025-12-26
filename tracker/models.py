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

class StudyRoom(models.Model):
    room_code = models.CharField(max_length=6, unique=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_rooms')
    partner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='joined_rooms')
    is_active = models.BooleanField(default=True)
    
    # Shared Timer State
    timer_start_time = models.DateTimeField(null=True, blank=True)
    timer_phase = models.CharField(max_length=20, default='study') # study, short_break, long_break
    timer_status = models.CharField(max_length=20, default='stopped') # running, paused, stopped
    timer_duration = models.IntegerField(default=25) # Duration in minutes
    paused_at = models.DateTimeField(null=True, blank=True)
    elapsed_time = models.DurationField(default=datetime.timedelta(0))
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Room {self.room_code} ({self.created_by.username})"

class PomodoroSession(models.Model):
    PHASE_CHOICES = [
        ('study', 'Study'),
        ('short_break', 'Short Break'),
        ('long_break', 'Long Break'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pomodoro_sessions')
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(null=True, blank=True)
    phase = models.CharField(max_length=20, choices=PHASE_CHOICES)
    cycle_number = models.IntegerField(default=1)
    is_completed = models.BooleanField(default=False)
    room = models.ForeignKey(StudyRoom, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.phase} - {self.start_time.date()}"
