from rest_framework import serializers
from ...models import Review

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'profile', 'product', 'rating', 'comment', "created_date", "updated_date"]