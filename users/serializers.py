from rest_framework import serializers
from users.models import Workout_User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workout_User
        fields = ["username", "email", "age", "weight", "password"]
