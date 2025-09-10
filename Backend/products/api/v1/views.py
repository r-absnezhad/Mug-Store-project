from rest_framework import viewsets
from rest_framework.response import Response    
from ...models import Product
from .productserializers import ProductSerializer
from .permissions import IsStaffOrReadOnly

class ProductModelViewSet(viewsets.ModelViewSet):
    """ 
    A viewset for viewing and editing product instances. 
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsStaffOrReadOnly]
