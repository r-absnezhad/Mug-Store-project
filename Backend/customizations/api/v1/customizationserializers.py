from rest_framework import serializers
from ...models import Customization, CustomizationSettings
class CustomizationSerializers(serializers.ModelSerializer):
    class Meta:
        model = Customization
        fields = ['id', 'product', 'user', 'custom_text', 'text_color', 'custom_image', 'placement_data', 'text_price', 'image_price',  'final_preview', 'created_date']
        read_only_fields = ['created_date', 'updated_date']


class CustomizationSettingsSerializers(serializers.ModelSerializer):
    class Meta:
        model = CustomizationSettings
        fields = ['id', 'text_price', 'image_price', 'created_date', 'updated_date']
        read_only_fields = ['created_date', 'updated_date']