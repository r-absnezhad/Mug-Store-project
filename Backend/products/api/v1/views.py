from rest_framework import viewsets
from rest_framework.response import Response    
from ...models import Product
from .productserializers import ProductSerializer
from .permissions import IsStaffOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
class ProductModelViewSet(viewsets.ModelViewSet):
    """ 
    A viewset for viewing and editing product instances. 
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsStaffOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_available',]
    search_fields = ['name', 'size']
    ordering_fields = ['name', 'size', 'base_price']

