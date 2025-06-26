from rest_framework import routers

from .views import AccountModelViewSet

router = routers.SimpleRouter()
router.register('', AccountModelViewSet, basename='accounts')

urlpatterns = [] + router.urls
