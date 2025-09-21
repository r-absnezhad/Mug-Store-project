from rest_framework import viewsets
from django.http import Http404
from django.utils.translation import gettext_lazy as _
from ..serializers import UserSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

from ..permissions import IsAuthenticatedOrAdmin

from django.contrib.auth import get_user_model
User = get_user_model()


class UserModelViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing user accounts.
    - Provides CRUD operations for user accounts.
    - Accessible only to authenticated users with admin privileges.
    - Supports filtering, searching, and ordering of user data.
    """
    permission_classes = [IsAuthenticatedOrAdmin]
    serializer_class = UserSerializer
    queryset = User.objects.all()

    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = {"username": ["exact", "in"], "email": ["exact", "in"]}
    search_fields = ["username", "email", "is_active", "is_verified"]
    ordering_fields = ["username", "email"]

    def get_object(self):
        """
        Retrieve a single user object based on the 'username' lookup field.
        - The `pk` in the URL is treated as the username.
        - Raises a 404 error if no user is found with the specified username.
        """
        lookup_field = "username"
        lookup_value = self.kwargs.get("pk")
        try:
            return self.queryset.get(**{lookup_field: lookup_value})
        except self.queryset.model.DoesNotExist:
            raise Http404(f"No user found with {lookup_field}={lookup_value}")



