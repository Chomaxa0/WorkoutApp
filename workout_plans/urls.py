from rest_framework.routers import DefaultRouter
from workout_plans.views import WeeklyWorkoutPlanViewSet

router = DefaultRouter()
router.register(r'weekly_workout', WeeklyWorkoutPlanViewSet, basename = 'weekly_workout')

urlpatterns = router.urls
