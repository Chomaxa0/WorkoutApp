from rest_framework import serializers
from exercises.models import Exercise


class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = ["name", "description", "instructions", "target_muscle", "equipment_required", "difficulty_level",
                  "category", "exercise_type", "calories_burned", "has_duration"]
