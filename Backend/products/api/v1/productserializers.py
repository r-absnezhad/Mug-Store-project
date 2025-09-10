
from rest_framework import serializers
from ...models import Product

class ProductSerializer(serializers.ModelSerializer):
    slug = serializers.ReadOnlyField()
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'size', 'slug', 'color', 'stock', 'image', 'is_available', 'base_price', 'created_date', 'updated_date']
        read_only_fields = ('created_date', 'updated_date')