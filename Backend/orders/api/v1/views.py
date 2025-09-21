from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated 
from ...models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

class OrderModelViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status',]
    search_fields = ['user__username', 'status']
    ordering_fields = ['created_date', 'user', 'status']


class OrderItemModelViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['product',]
    ordering_fields = ['product', 'price',]

