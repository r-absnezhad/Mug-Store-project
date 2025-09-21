from django.urls import path, include
from rest_framework import routers
from .views import OrderModelViewSet, OrderItemModelViewSet

router = routers.SimpleRouter()
router.register(r'orders', OrderModelViewSet)
# what is the different?
router.register(r'order-items', OrderItemModelViewSet)


urlpatterns = [
    path('', include(router.urls)),
]