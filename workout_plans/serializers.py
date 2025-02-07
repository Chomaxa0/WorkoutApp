from rest_framework import serializers
from workout_plans.models import WorkoutPlanWorkout, WeeklyWorkoutPlan
from workouts.models import Workout


class WorkoutPlanWorkoutSerializer(serializers.ModelSerializer):
    workout_id = serializers.PrimaryKeyRelatedField(queryset = Workout.objects.all(), source = 'workout')

    class Meta:
        model = WorkoutPlanWorkout
        fields = ['workout_id', 'repetitions_per_week']


class WeeklyWorkoutPlanSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default = serializers.CurrentUserDefault())
    workouts = WorkoutPlanWorkoutSerializer(many = True)

    total_weekly_calories = serializers.SerializerMethodField(read_only = True)
    weeks_till_calorie_goal = serializers.SerializerMethodField(read_only = True)

    class Meta:
        model = WeeklyWorkoutPlan
        fields = ['id', 'name', 'user', 'created_at', 'workouts','total_weekly_calories','weeks_till_calorie_goal']

    def create(self, validated_data):
        workouts_data = validated_data.pop('workouts', [])
        weekly_workout_plan = WeeklyWorkoutPlan.objects.create(name = validated_data['name'], user = validated_data['user'])

        for workout_data in workouts_data:

            workout = workout_data['workout']
            if workout.user != self.context['request'].user:
                raise serializers.ValidationError("You do not have permission to update this object.")
            repetitions_per_week = workout_data['repetitions_per_week']
            WorkoutPlanWorkout.objects.create(plan = weekly_workout_plan, workout = workout,
                                              repetitions_per_week = repetitions_per_week)

        return weekly_workout_plan

    def update(self, instance, validated_data):
        user = self.context['request'].user
        if instance.user != user:
            raise serializers.ValidationError("You do not have permission to update this object.")

        workouts_data = validated_data.pop('workouts', [])
        instance.name = validated_data.get('name', instance.name)
        instance.save()

        for workout_data in workouts_data:
            workout = workout_data['workout']
            repetitions_per_week = workout_data['repetitions_per_week']
            plan_workout, created = WorkoutPlanWorkout.objects.get_or_create(
                plan = instance, workout = workout
            )
            plan_workout.repetitions_per_week = repetitions_per_week
            plan_workout.save()

        return instance

    def get_total_weekly_calories(self, obj):
        workouts_data = obj.workouts.all()
        total_weekly_calories = 0
        for workout_data in workouts_data:
            workout = workout_data.workout
            total_weekly_calories += workout.total_calories * workout_data.repetitions_per_week
        return total_weekly_calories

    def get_weeks_till_calorie_goal(self, obj):
        if  obj.user.goal_calories is None:
            return None

        calories = obj.user.calories
        weekly_calories = self.get_total_weekly_calories(obj)
        goal_calories = obj.user.goal_calories
        result = round((goal_calories - calories) / weekly_calories, 1)
        return 0 if result < 0 else result
    

class SetWorkoutGoalSerializer(serializers.Serializer):
    goal_calories = serializers.IntegerField(min_value=0, required=True)
    
    
