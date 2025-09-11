from rest_framework import viewsets
from customizationserializers import CustomizationSerializers
from ...models import Customization
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import filters

class CustomizationModelViewSet(viewsets.ModelViewSet):
    queryset = Customization.objects.all()
    serializer_class = CustomizationSerializers
    permission_classes = [IsAuthenticated] 
    filter_backends = [SearchFilter, OrderingFilter ]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['user__username', 'product']
    ordering_fields = ['user', 'product', '-created_at']
