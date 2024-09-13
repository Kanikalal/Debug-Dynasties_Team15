from django.db import models
from django.contrib.auth.models import User

class Exercise(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    muscle_group = models.CharField(max_length=50)
    fitness_level = models.CharField(max_length=50)
    equipment = models.CharField(max_length=100)
    image_url = models.URLField()

    def __str__(self):
        return self.name

class WorkoutPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateField(auto_now_add=True)
    exercises = models.ManyToManyField(Exercise)

    def __str__(self):
        return f'{self.user.username} - {self.date_created}'
