from rest_framework import routers

from apps.documents.views import DocumentModelViewSet

router = routers.SimpleRouter()
router.register("", DocumentModelViewSet, basename="documents")

urlpatterns = [] + router.urls
