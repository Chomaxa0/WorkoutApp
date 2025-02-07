from django.db import models

class Exercise(models.Model):
    EXERCISE_TYPES = [
        ('ST', 'Strength Training'),
        ('CA', 'Cardio'),
        ('FL', 'Flexibility'),
        ('BA', 'Balance'),
    ]

    DIFFICULTY_CHOICES = [
        ('Beg', 'Beginner'),
        ('Int', 'Intermediate'),
        ('Adv', 'Advanced'),
    ]

    MUSCLE_GROUPS = [
        ("Chest", "Chest"),
        ("Back", "Back"),
        ("Legs", "Legs"),
        ("Core", "Core"),
    ]

    name = models.CharField(max_length = 100)
    description = models.TextField()
    instructions = models.TextField()
    target_muscle = models.CharField(
        max_length = 10,
        choices = MUSCLE_GROUPS,
    )
    equipment_required = models.CharField(max_length = 255, blank = True, null = True)
    difficulty_level = models.CharField(
        max_length = 3,
        choices = DIFFICULTY_CHOICES,
    )
    category = models.CharField(max_length = 50)
    exercise_type = models.CharField(
        max_length = 2,
        choices = EXERCISE_TYPES,
    )
    calories_burned = models.IntegerField(blank = True, null = True)
    has_duration = models.BooleanField(blank = False, null = False)
    
