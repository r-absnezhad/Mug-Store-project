from rest_framework import serializers
from ....models import Order

class OrderSerializer(serializers.ModelSerializer):
    total_price = serializers.DecimalField(max_digits=8, decimal_places=2, read_only=True)
    class Meta:
        model = Order
        fields = ['id', 'user', 'total_price', 'status', 'item_count', 'created_date', 'updated_date']
        read_only_fields = ('created_date', 'updated_date')
