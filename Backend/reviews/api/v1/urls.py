from django.urls import path, include
from rest_framework import routers
from .views import ReviewModelViewSet


router = routers.SimpleRouter()
router.register('reviews', ReviewModelViewSet, basename='review')
urlpatterns = [
    path('', include(router.urls)),
]
