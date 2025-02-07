from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.core.management import call_command
from exercises.models import Exercise


@receiver(post_migrate)
def seed_exercises_after_migrate(sender, **kwargs):
    if Exercise.objects.count() == 0:
        print("Migrating exercises...")
        call_command('seed_exercises')
    else:
        print("Exercises already seeded.")
