from rest_framework import serializers
from ...models import Customization
class CustomizationSerializers(serializers.ModelSerializer):
    class Meta:
        Model = Customization
        fields = []
