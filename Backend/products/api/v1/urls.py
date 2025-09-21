from django.urls import path, include
from rest_framework import routers
from .views import ProductModelViewSet

router = routers.SimpleRouter()
router.register(r'products', ProductModelViewSet, basename='product')

urlpatterns = [
    path('', include(router.urls)),
]