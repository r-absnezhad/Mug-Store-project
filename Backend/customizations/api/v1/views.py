from rest_framework import viewsets
from .customizationserializers import CustomizationSerializers, CustomizationSettingsSerializers
from ...models import Customization, CustomizationSettings
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import filters
from .permissions import IsStaffOrReadOnly
class CustomizationModelViewSet(viewsets.ModelViewSet):
    queryset = Customization.objects.all()
    serializer_class = CustomizationSerializers
    permission_classes = [IsAuthenticated] 
    filter_backends = [SearchFilter, OrderingFilter ]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['user__username', 'product']
    ordering_fields = ['user', 'product', '-created_at']


class CustomizationSettingsModelViewSet(viewsets.ModelViewSet): 
    queryset = CustomizationSettings.objects.all()
    serializer_class = CustomizationSettingsSerializers
    permission_classes = [IsStaffOrReadOnly] 
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['text_price', 'image_price', '-created_date']