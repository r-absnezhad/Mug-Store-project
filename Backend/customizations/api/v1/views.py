from rest_framework import viewsets
from customizationserializers import CustomizationSerializers
from ...models import Customization
from rest_framework.permissions import IsAuthenticated



class CustomizationModelViewSet(viewsets.ModelViewSet):
    queryset = Customization.objects.all()
    serializer_class = CustomizationSerializers
    permission_classes = [IsAuthenticated] 
    filter_backends