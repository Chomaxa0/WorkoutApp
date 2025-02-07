from rest_framework.routers import DefaultRouter
from exercises.views import ExerciseViewSet

router = DefaultRouter()
router.register(r'exercises', ExerciseViewSet, basename = 'exercise')

urlpatterns = router.urls
