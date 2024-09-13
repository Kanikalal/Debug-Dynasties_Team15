from django.db import models
from django.contrib.auth.models import User

class Workout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    exercise_type = models.CharField(max_length=100)
    duration_minutes = models.PositiveIntegerField()
    calories_burned = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.user.username} - {self.exercise_type} on {self.date}'
