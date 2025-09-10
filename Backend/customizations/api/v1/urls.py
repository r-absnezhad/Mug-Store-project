from rest_framework.routers import SimpleRouter
from views import CustomizationModelViewSet
from django.urls import path, include


router = SimpleRouter()
router.register(r'customizations', CustomizationModelViewSet)
urlpatterns = [
    path('', include(router.urls))
]