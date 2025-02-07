from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from users.models import Workout_User
from users.serializers import UserSerializer


class RegisterUserView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        username = request.data.get("username")
        email = request.data.get("email")
        password = request.data.get("password")
        age = request.data.get("age")
        calories = request.data.get("calories", 0)
        weight = request.data.get("weight")

        if not username or not password:
            return Response({ "error":"Username and password are required" }, status = status.HTTP_400_BAD_REQUEST)

        if Workout_User.objects.filter(username = username).exists():
            return Response({ "error":"Username already exists" }, status = status.HTTP_400_BAD_REQUEST)

        if Workout_User.objects.filter(email = email).exists():
            return Response({ "error":"Email already exists" }, status = status.HTTP_400_BAD_REQUEST)

        user = Workout_User.objects.create_user(username = username, email = email, password = password, age = age,
                                                calories = calories, weight = weight)
        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "user":UserSerializer(user).data,
                "refresh":str(refresh),
                "access":str(refresh.access_token),
            },
            status = status.HTTP_201_CREATED,
        )
