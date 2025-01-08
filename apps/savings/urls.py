from rest_framework import routers

from apps.savings.views import SavingModelViewSet, GoalModelViewSet

router = routers.SimpleRouter()
router.register('goals', GoalModelViewSet)
router.register('', SavingModelViewSet)

urlpatterns = router.urls
