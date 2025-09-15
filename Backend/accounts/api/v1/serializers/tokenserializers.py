from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from django.contrib.auth import get_user_model
User = get_user_model()



# class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
#     """
#     Custom serializer for obtaining JWT access and refresh tokens.
#     This serializer extends the default TokenObtainPairSerializer to add
#     additional checks and return extra user details (email and user_id)
#     alongside the tokens.
#     """

#     def validate(self, attrs):
#         """
#         Validate the user credentials and check if the user is verified.
#         If the user is not verified, raise a validation error.
#         If the user is verified, return the validated data with additional
#         information (email and user_id).
#         """
#         validated_data = super().validate(attrs)
#         if not self.user.is_verified:
#             raise serializers.ValidationError({"details": "User is not verified."})
#         validated_data["email"] = self.user.email
#         validated_data["user_id"] = self.user.id
#         return validated_data


class CustomAuthTokenSerializer(serializers.Serializer):
    """
    Custom serializer for user authentication and token generation.
    This serializer takes user credentials (email and password),
    authenticates the user, and if successful, generates a token.
    """

    username = serializers.CharField(label=_("Username"), write_only=True)
    password = serializers.CharField(
        label=_("Password"),
        style={"input_type": "password"},
        trim_whitespace=False,
        write_only=True,
    )
    token = serializers.CharField(label=_("Token"), read_only=True)

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        if username and password:
            user = authenticate(
                request=self.context.get("request"),
                username=username,
                password=password,
            )

            if not user:
                msg = _("Unable to log in with provided credentials.")
                raise serializers.ValidationError(msg, code="authorization")
            if not user.is_verified:
                raise serializers.ValidationError({"details": "User is not verified."})

        else:
            msg = _('Must include "username" and "password" .')
            raise serializers.ValidationError(msg, code="authorization")

        attrs["user"] = user
        return attrs



class RegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for registering a new user, including validation of password and email.
    """
    password1 = serializers.CharField(max_length=255, write_only=True)
    class Meta:
        model = User
        fields = ["email", "username", "password", "password1"]

    def validate(self, attrs):
        if attrs.get("password") != attrs.get("password1"):
            raise serializers.ValidationError({"detail": "passwords must be the same"})
        try:
            validate_password(attrs.get("password"))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})
        return super().validate(attrs)
    
    def create(self, validated_data):
        validated_data.pop("password1", None)
        return User.objects.create_user(**validated_data)


