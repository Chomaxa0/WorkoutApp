from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField
from exercises.models import Exercise
from exercises.serializers import ExerciseSerializer
from workouts.models import Workout, WorkoutExercise, WorkoutHistory, WorkoutSession
from workouts.services import WorkoutService


class WorkoutExerciseSerializer(serializers.ModelSerializer):
    
    exercise = PrimaryKeyRelatedField(queryset = Exercise.objects.all())

    class Meta:
        model = WorkoutExercise
        fields = ['exercise', 'reps', 'sets', 'duration']

    def validate(self, data):
        sets = data.get('sets')
        reps = data.get('reps')
        duration = data.get('duration')
        exercise = data.get('exercise')

        if exercise.has_duration and duration is None:
            raise serializers.ValidationError('duration cannot be None for this exercise')
        if exercise.has_duration is False and reps is None:
            raise serializers.ValidationError('reps cannot be None for this exercise')

        if reps is not None and sets is not None and duration is not None:
            raise serializers.ValidationError(
                "You cannot provide 'reps', 'sets' and 'duration' for an exercise simultaneously.")

        if reps is not None and duration is not None:
            raise serializers.ValidationError("You cannot provide both 'reps' and 'duration' for an exercise.")

        if reps is not None and sets is None:
            raise serializers.ValidationError("You cannot provide both 'reps' without 'sets' for an exercise.")

        return data


class WorkoutSerializer(serializers.ModelSerializer):
    exercises = WorkoutExerciseSerializer(many = True, write_only = True)
    user = serializers.HiddenField(default = serializers.CurrentUserDefault())

    class Meta:
        model = Workout
        fields = ['id', 'name', 'description', 'exercises', 'user']

    def validate_exercises(self, exercises_data):
        if len(exercises_data) == 0:
            raise serializers.ValidationError("Please enter at least one exercise")

        exercise_ids = [exercise['exercise'].id for exercise in exercises_data]
        if len(exercise_ids) != len(set(exercise_ids)):  # Check for duplicates
            raise serializers.ValidationError("Duplicate exercises found in the workout.")
        return exercises_data

    def create(self, validated_data):
        exercises_data = validated_data.get('exercises')
        workout = WorkoutService.create_workout_with_exercises(
            user = validated_data["user"],
            name = validated_data["name"],
            description = validated_data["description"],
            exercises_data = exercises_data)

        return workout

    def update(self, instance, validated_data):

        user = self.context['request'].user
        if validated_data.user != user:
            raise serializers.ValidationError("You do not have permission to update this object.")

        exercises_data = validated_data.get('exercises', [])

        workout = WorkoutService.update_workout(
            workout_id = instance.id,
            user = self.context['request'].user,
            name = validated_data.get('name', instance.name),
            description = validated_data.get('description', instance.description),
            exercises_data = exercises_data
        )

        return workout


class WorkoutHistorySerializer(serializers.ModelSerializer):

    workout = WorkoutSerializer(many = False, read_only = True)
    class Meta:
        model = WorkoutHistory
        fields = ["initial_calories","calories_burned","completed_at","workout"]


class WorkoutSessionSerializer(serializers.ModelSerializer):
    current_exercise = ExerciseSerializer()
    next_exercise = serializers.SerializerMethodField()

    class Meta:
        model = WorkoutSession
        fields = ['current_exercise', 'next_exercise']

    def get_next_exercise(self, obj):
        next_exercise = obj.get_next_exercise()
        if next_exercise:
            return ExerciseSerializer(next_exercise.exercise).data
        return None