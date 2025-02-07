from django.db import models
from exercises.models import Exercise
from users.models import Workout_User


class Workout(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    user = models.ForeignKey(Workout_User, related_name="workouts",
                             on_delete=models.CASCADE)  # Many-to-Many relationship
    exercises = models.ManyToManyField(Exercise, through="WorkoutExercise")  # Intermediate model
    total_calories = models.PositiveIntegerField(default=0)

    def __str__(self):
        return str(self.name)


class WorkoutExercise(models.Model):
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    reps = models.PositiveIntegerField(blank=True, null=True)  # Used for rep-based exercises
    sets = models.PositiveIntegerField(blank=True, null=True)  # Number of sets
    duration = models.DurationField(blank=True, null=True)  # Used for duration-based exercises

    def __str__(self):
        return f"{self.workout.name} - {self.exercise.name}"


class WorkoutHistory(models.Model):
    workout = models.ForeignKey(Workout, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(Workout_User, on_delete=models.CASCADE)
    initial_calories = models.PositiveIntegerField()
    calories_burned = models.PositiveIntegerField()
    completed_at = models.DateTimeField(auto_now_add=True)


class WorkoutSession(models.Model):
    user = models.ForeignKey(Workout_User, on_delete=models.CASCADE)
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    current_exercise = models.ForeignKey(WorkoutExercise, on_delete=models.SET_NULL, null=True, blank=True)
    completed_exercises = models.ManyToManyField(WorkoutExercise, related_name="completed_sessions")
    start_time = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def get_current_exercise(self):
        return self.current_exercise

    def get_next_exercise(self):
        workout_exercises = list(self.workout.workoutexercise_set.all())
        current_index = workout_exercises.index(self.current_exercise)
        if current_index < len(workout_exercises) - 1:
            return workout_exercises[current_index + 1]
        return None

    def complete_exercise(self, exercise):
        self.completed_exercises.add(exercise)

        next_exercise = WorkoutExercise.objects.filter(workout=self.workout).exclude(
            id__in=self.completed_exercises.all()).first()
        self.current_exercise = next_exercise
        if not next_exercise:
            self.is_active = False
        self.save()
