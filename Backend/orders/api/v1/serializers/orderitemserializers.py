from rest_framework import serializers
from ....models import Order, OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    total_price = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product', 'customization', 'quantity', 'price', 'total_price']
        read_only_fields = ('created_date', 'updated_date')
