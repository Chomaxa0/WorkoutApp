from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets, permissions, status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.decorators import action
from workout_plans.models import WeeklyWorkoutPlan
from workout_plans.serializers import WeeklyWorkoutPlanSerializer, SetWorkoutGoalSerializer


@extend_schema_view(
    list=extend_schema(
        summary="List all weekly workout plans",
        description="Returns a list of weekly workout plans for the authenticated user.",
        responses={200: WeeklyWorkoutPlanSerializer(many=True)}
    ),
    retrieve=extend_schema(
        summary="Retrieve a weekly workout plan",
        description="Fetches the details of a specific weekly workout plan by ID.",
        responses={200: WeeklyWorkoutPlanSerializer}
    ),
    destroy=extend_schema(
        summary="Delete a weekly workout plan",
        description="Deletes a weekly workout plan for the authenticated user.",
        responses={204: {"description": "Weekly workout plan deleted successfully"}}
    ),
)


class WeeklyWorkoutPlanViewSet(viewsets.ModelViewSet):
    serializer_class = WeeklyWorkoutPlanSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return WeeklyWorkoutPlan.objects.filter(user=self.request.user)

    def get_object(self):
        queryset = self.get_queryset()
        try:
            obj = queryset.get(pk=self.kwargs['pk'], user=self.request.user)
        except WeeklyWorkoutPlan.DoesNotExist:
            raise NotFound(detail="Weekly workout plan not found or not accessible.")
        return obj

    @extend_schema(
        summary="Set user workout calorie goal",
        request=SetWorkoutGoalSerializer,
        responses={200: {"type": "object", "properties": {"message": {"type": "string"}, "calories": {"type": "integer"}}}},
        description="Sets the user's workout calorie goal.",
    )
    @action(detail=False, methods=["post"], permission_classes=[permissions.IsAuthenticated])
    def set_user_workout_goal(self, request):
        user = self.request.user
        try:
            calories = int(request.data.get("goal_calories"))
            if calories < 0:
                return Response({"error": "Calories must be a positive number"}, status=status.HTTP_400_BAD_REQUEST)
        except (ValueError, TypeError):
            return Response({"error": "Invalid value for calories"}, status=status.HTTP_400_BAD_REQUEST)

        user.goal_calories = calories
        user.save()

        return Response({"message": "Calories updated successfully", "calories": user.goal_calories})
