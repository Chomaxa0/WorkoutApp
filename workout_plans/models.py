from django.db import models
from users.models import Workout_User
from workouts.models import Workout


class WeeklyWorkoutPlan(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(Workout_User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class WorkoutPlanWorkout(models.Model):
    plan = models.ForeignKey(WeeklyWorkoutPlan, on_delete=models.CASCADE, related_name="workouts")
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    repetitions_per_week = models.PositiveIntegerField(default=1)
