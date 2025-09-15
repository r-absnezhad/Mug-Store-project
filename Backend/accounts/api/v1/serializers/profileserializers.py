from rest_framework import serializers
from ....models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'user', 'gender', 'image', 'first_name', 'last_name', 'phone_number', 'birth_date', 'created_date', 'updated_date']




# class UpdateProfileSerializer(serializers.ModelSerializer):
#     """
#     Serializer to update the phone number of a profile.
#     """

#     phone_number = serializers.CharField(
#         required=True, allow_blank=False, write_only=True
#     )
#     first_name = serializers.CharField(
#         required=True, allow_blank=False, write_only=True
#     )
#     last_name = serializers.CharField(required=True, allow_blank=False, write_only=True)

#     class Meta:
#         model = Profile
#         fields = ["phone_number", "first_name", "last_name"]

#     def validate(self, value):
#         phone = value["phone_number"]
#         first_name = value["first_name"]
#         last_name = value["last_name"]
#         if not phone:
#             raise serializers.ValidationError("Phone number is required.")
#         if not phone.isdigit():
#             raise serializers.ValidationError("Phone number must contain only digits.")
#         if len(phone) != 11:
#             raise serializers.ValidationError(
#                 "Phone number must be at least 10 digits."
#             )

#         if not first_name:
#             raise serializers.ValidationError("First name is required.")
#         if not first_name.isalpha():
#             raise serializers.ValidationError("First name must contain only character.")

#         if not last_name:
#             raise serializers.ValidationError("last name is required.")
#         if not last_name.isalpha():
#             raise serializers.ValidationError("last name must contain only character.")
#         return value
