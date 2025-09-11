from rest_framework import serializers
from ...models import Customization
class CustomizationSerializers(serializers.ModelSerializer):
    class Meta:
        model = Customization
        fields = ['id', 'product', 'user', 'custom_text', 'text_color', 'custom_image', 'placement', 'created_at']
