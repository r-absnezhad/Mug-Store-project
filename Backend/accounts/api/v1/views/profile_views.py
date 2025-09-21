
from rest_framework import generics
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from rest_framework.response import Response
from ..serializers import (
    ProfileSerializer,
    UpdateProfileSerializer,
)
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from ....models import Profile
from django.contrib.auth import get_user_model
User = get_user_model()


class ProfileListApiView(generics.ListAPIView):
    """
    API view for listing all profiles.
    - Provides a read-only endpoint for listing all profile records in the database.
    - Accessible only to authenticated admin users.
    - Supports filtering, searching, and ordering.
    """

    permission_classes = [IsAdminUser, IsAuthenticated]
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["phone_number", "last_name", "first_name"]
    search_fields = [ "phone_number", "first_name", "last_name"]
    ordering_fields = ["last_name", "first_name"]



class CheckProfileApiView(APIView):
    """
    View to check whether the authenticated user has all information in their profile.

    This view allows users to verify if their profile contains all needed information. It is a read-only operation
    and requires the user to be authenticated.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile = get_object_or_404(Profile, user__username=request.user.username)
        data = {
            "has_all_information": bool(
                profile.first_name and profile.last_name and profile.phone_number
            ),
        }
        return Response(data)


class ProfileRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    """
    API view for retrieving and updating the authenticated user's profile.
    - Allows users to view and update their own profile information.
    """
    queryset = Profile.objects.all()
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.profile

    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            return UpdateProfileSerializer
        return ProfileSerializer


