from rest_framework.routers import DefaultRouter
from workouts.views import WorkoutViewSet

router = DefaultRouter()
router.register(r'workouts', WorkoutViewSet, basename = 'workout')

urlpatterns = router.urls
