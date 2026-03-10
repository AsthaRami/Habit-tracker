from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Habit(models.Model):
    FREQUENCY_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    frequency = models.CharField(max_length=10, choices=FREQUENCY_CHOICES, default='daily')
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def get_streak(self):
        logs = self.habitlog_set.filter(completed=True).order_by('-date')
        streak = 0
        today = timezone.now().date()
        for i, log in enumerate(logs):
            expected = today - timezone.timedelta(days=i)
            if log.date == expected:
                streak += 1
            else:
                break
        return streak

class HabitLog(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    completed = models.BooleanField(default=False)
    notes = models.TextField(blank=True)

    class Meta:
        unique_together = ('habit', 'date')

    def __str__(self):
        return f'{self.habit.name} - {self.date}'
