from rest_framework import serializers
from ....models import CustomUser 
from django.core import exceptions
from django.contrib.auth.password_validation import validate_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'is_active', 'is_staff', 'is_superuser', 'created_date', 'updated_date']





class CustomChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for changing the user's password.
    This serializer ensures the old password is valid, and the new password meets the requirements.
    It also ensures that the new passwords match before saving the new password.
    """

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    new_password1 = serializers.CharField(required=True)

    def validate(self, attrs):
        """
        Validate the passwords provided by the user.
        - Checks that the new password and its confirmation match.
        - Validates the new password against Django's password validation rules.
        """

        if attrs.get("new_password") != attrs.get("new_password1"):
            raise serializers.ValidationError({"detail": "passwords must be the same"})
        try:
            validate_password(attrs.get("new_password"))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({"new_password": list(e.messages)})
        return super().validate(attrs)


