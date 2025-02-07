from rest_framework import viewsets, permissions
from exercises.models import Exercise
from exercises.serializers import ExerciseSerializer


class ExerciseViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ExerciseSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Exercise.objects.all()
