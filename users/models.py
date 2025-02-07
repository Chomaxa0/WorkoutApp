from django.contrib.auth.models import AbstractUser
from django.db import models


class Workout_User(AbstractUser):
    age = models.PositiveIntegerField()
    calories = models.PositiveIntegerField(default=0)
    weight = models.PositiveIntegerField()
    goal_calories = models.PositiveIntegerField(blank=True, null=True)
