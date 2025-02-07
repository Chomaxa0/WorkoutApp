from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from exercises.models import Exercise
from exercises.serializers import ExerciseSerializer
from workouts.models import Workout, WorkoutExercise, WorkoutHistory, WorkoutSession


class WorkoutService:

    @staticmethod
    def get_workouts_for_user(user):
        return Workout.objects.filter(user = user)

    @staticmethod
    def create_workout_with_exercises(name, description, exercises_data, user):
        try:
            with (transaction.atomic()):

                workout = Workout.objects.create(
                    name = name,
                    description = description,
                    user = user,
                )

                total_calories = 0
                workout_exercises = []
                for exercise in exercises_data:
                    reps = exercise.get('reps')
                    sets = exercise.get('sets')
                    duration = exercise.get('duration')

                    current_exercise = Exercise.objects.get(pk = exercise.get('exercise').id)
                    workout_exercise = WorkoutExercise(workout = workout, reps = reps,
                                                       sets = sets, duration = duration,
                                                       exercise = current_exercise)

                    if not current_exercise.has_duration:
                        total_calories += (reps * sets) * current_exercise.calories_burned

                    if current_exercise.has_duration:
                        total_calories += current_exercise.calories_burned * (duration.seconds / 60) * sets

                    workout_exercises.append(workout_exercise)

                WorkoutExercise.objects.bulk_create(workout_exercises)
                workout.total_calories = total_calories
                workout.save()
                return workout

        except Exception as e:
            print(f"Error: {e}")
            raise e

    @staticmethod
    def update_workout(workout_id, user, name=None, description=None, exercises_data=None):
        try:
            workout = Workout.objects.filter(id = workout_id, user = user).first()
            if not workout:
                raise ObjectDoesNotExist("Workout not found")

            with transaction.atomic():
                if name:
                    workout.name = name
                if description:
                    workout.description = description
                workout.save()

                if exercises_data is not None:
                    WorkoutExercise.objects.filter(workout = workout).delete()

                    workout_exercises = []
                    for exercise in exercises_data:
                        exercise_obj = Exercise.objects.get(pk = exercise.get('exercise').id)
                        workout_exercise = WorkoutExercise(
                            workout = workout,
                            reps = exercise.get('reps'),
                            sets = exercise.get('sets'),
                            duration = exercise.get('duration'),
                            exercise = exercise_obj
                        )
                        workout_exercises.append(workout_exercise)

                    WorkoutExercise.objects.bulk_create(workout_exercises)

                return workout

        except ObjectDoesNotExist as e:
            return Response({"error: workout not found"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(f"Error updating workout: {e}")
            raise e

    @staticmethod
    def get_workout_details(workout_id, user):
        try:
            workout = Workout.objects.get(pk = workout_id, user = user)
            workout_exercises = WorkoutExercise.objects.filter(workout = workout)

            exercises_data = []
            for workout_exercise in workout_exercises:
                exercise = workout_exercise.exercise
                exercises_data.append({
                    "exercise":{
                        "exercise":exercise.id,
                        "name":exercise.name,
                        "description":exercise.description,
                        "target_muscle":exercise.target_muscle,
                        "difficulty_level":exercise.difficulty_level,
                        "category":exercise.category,
                        "exercise_type":exercise.exercise_type,
                        "calories_burned":exercise.calories_burned,
                    },
                    "reps":workout_exercise.reps,
                    "sets":workout_exercise.sets,
                    "duration":workout_exercise.duration,
                })

            response_data = {
                "id":workout.id,
                "name":workout.name,
                "description":workout.description,
                "user":workout.user.id,
                "total_calories":workout.total_calories,
                "exercises":exercises_data
            }

            return Response(response_data, status = status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({ "error":"workout not found" }, status = status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({ "error": str(e) }, status = status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def get_workout_history(user):
        return  WorkoutHistory.objects.filter(user = user)

    @staticmethod
    def get_current_session_exercise(session_id, user):
        try:
            session = WorkoutSession.objects.get(pk=session_id, user=user, is_active = True)
            if session is None or not session.is_active:
                return Response({ "message":"Workout not started" }, status = status.HTTP_400_BAD_REQUEST)

            current_exercise = session.get_current_exercise()
            next_exercise = session.get_next_exercise()

            data = {
                "current_exercise":
                    {"exercise": ExerciseSerializer(current_exercise.exercise).data,
                     "reps":current_exercise.reps,
                     "sets":current_exercise.sets,
                     "duration":current_exercise.duration},
                "next_exercise": next_exercise and   {"exercise": ExerciseSerializer(next_exercise.exercise).data,
                     "reps":next_exercise.reps,
                     "sets":next_exercise.sets,
                     "duration":next_exercise.duration},
            }

            return Response(data)
        except ObjectDoesNotExist:
            return Response({ "message":"Active workout session not found" }, status = status.HTTP_404_NOT_FOUND)

    @staticmethod
    def complete_exercise(session_id, user):
        try:
            with transaction.atomic():
                session = WorkoutSession.objects.get(pk = session_id, user = user, is_active = True)
                if not session.current_exercise:
                    return Response({ "message":"No exercise to complete" }, status = status.HTTP_400_BAD_REQUEST)

                session.complete_exercise(session.current_exercise)

                if not session.is_active:
                    workout_calories = session.workout.total_calories
                    WorkoutHistory.objects.create(user = user, workout_id = session.workout_id,initial_calories = user.calories, calories_burned = workout_calories)
                    user.calories += workout_calories
                    user.save()

                return Response({
                    "message":"Exercise completed",
                    "next_exercise":session.current_exercise.exercise.name if session.current_exercise else None,
                    "is_workout_finished":not session.is_active
                }, status = status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({ "error":"Active workout session not found" }, status = status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({ "error": str(e) }, status = status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def start_workout(workout_id, user):
        try:
            workout = Workout.objects.get(pk = workout_id, user = user)
            if WorkoutSession.objects.filter(workout = workout, is_active = True).exists():
                return Response({ "detail":"Workout already started" }, status = status.HTTP_200_OK)
            if WorkoutSession.objects.filter(user = user, is_active = True).exists():
                return Response({ "message":"User already has active workout" }, status = status.HTTP_200_OK)
            with transaction.atomic():
                session = WorkoutSession.objects.create(user = user, workout = workout)

                session.current_exercise = workout.workoutexercise_set.first()
                session.is_active = True
                session.save()

                return Response({
                    "session_id":session.id,
                    "workout":workout.name,
                    "current_exercise":session.current_exercise.exercise.name if session.current_exercise else None
                }, status = status.HTTP_201_CREATED)
        except ObjectDoesNotExist:
            return Response({ "error":"workout not found" }, status = status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({ "error": str(e) }, status = status.HTTP_400_BAD_REQUEST)