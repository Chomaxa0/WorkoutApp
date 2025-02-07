
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from workouts.serializers import WorkoutSerializer, WorkoutHistorySerializer, WorkoutSessionSerializer
from workouts.models import Workout
from workouts.services import WorkoutService

@extend_schema_view(
    list=extend_schema(
        summary="List all workouts",
        description="Returns a list of workouts belonging to the authenticated user.",
        responses={200: WorkoutSerializer(many=True)}
    ),
    retrieve=extend_schema(
        summary="Retrieve a workout",
        description="Fetches the details of a specific workout by ID.",
        responses={200: WorkoutSerializer}
    ),
    destroy=extend_schema(
        summary="Delete a workout",
        description="Deletes a workout and all associated history, exercises, and sessions.",
        responses={204: {"description": "Workout deleted successfully"}}
    ),
)
class WorkoutViewSet(viewsets.ModelViewSet):
    serializer_class = WorkoutSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Workout.objects.filter(user=self.request.user)

    @extend_schema(
        summary="Create a new workout",
        description="Creates a new workout for the authenticated user.",
        responses={201: WorkoutSerializer},
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @extend_schema(
        summary="Update an existing workout",
        description="Updates a workout instance with new details.",
        responses={200: WorkoutSerializer}
    )
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        return WorkoutService.get_workout_details(kwargs.get('pk'), request.user)

    @extend_schema(
        summary="Get workout history",
        description="Retrieves the history of completed workouts for the authenticated user.",
        responses={200: WorkoutHistorySerializer(many=True)}
    )
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def workout_history(self, request):
        workout_history = WorkoutService.get_workout_history(request.user)
        serialized = WorkoutHistorySerializer(workout_history, many=True).data
        return Response(serialized, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Start a workout session",
        description="Starts a workout session and logs it in the history.",
        request=None,
        responses={200: {"description": "Workout started"}}
    )
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def start_workout(self, request, pk=None):
        return WorkoutService.start_workout(pk, request.user)

    @extend_schema(
        summary="Mark an exercise as complete",
        description="Marks an exercise in the workout as complete, logging the completion.",
        request=None,
        responses={200: {"description": "Exercise marked as complete"}}
    )
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def complete_exercise(self, request, pk=None):
        return WorkoutService.complete_exercise(pk, request.user)

    @extend_schema(
        summary="Get current and next exercise in the workout session",
        description="Returns the current exercise and the next exercise to do based on the workout session, along with detailed information about each exercise.",
        responses={200: WorkoutSessionSerializer}
    )
    @action(detail=True, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def get_current_exercise(self, request, pk=None):
        return WorkoutService.get_current_session_exercise(pk, request.user)

