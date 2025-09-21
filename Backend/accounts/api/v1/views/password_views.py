
from rest_framework import generics
from rest_framework import status
from django.utils.translation import gettext_lazy as _
from rest_framework.response import Response
from ..serializers import CustomChangePasswordSerializer

from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
User = get_user_model()
from django.urls import reverse_lazy

from django.conf import settings
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from django.conf import settings



class CustomChangePasswordApiView(generics.GenericAPIView):
    """
    API view for handling user password changes.
    This view allows authenticated users to change their password by providing
    their current password and a new password.
    """

    serializer_class = CustomChangePasswordSerializer
    permission_classes = [IsAuthenticated]
    model = User

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def put(self, request, *args, **kwargs):
        """
        Handle PUT requests to change the user's password.
        - Validates the old password.
        - Ensures the new password is different from the old password.
        - Saves the new password and updates the user's state.
        """
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response(
                    {"old_password": "Wrong password"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if serializer.data.get("old_password") == serializer.data.get(
                "new_password"
            ):
                return Response(
                    {"new_password": "passwords must be different"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response(
                {"details": "Password changed successfully"},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomPasswordResetView(PasswordResetView):
    """
    A custom password reset view that extends Django's built-in PasswordResetView.
    """
    template_name = 'registration/password_reset_form.html'
    email_template_name = 'registration/password_reset_email.html'
    subject_template_name = 'registration/password_reset_subject.txt'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy("accounts:custom_password_reset_done")
    extra_email_context = {
        "domain": settings.DEFAULT_DOMAIN,
        "protocol": settings.DEFAULT_PROTOCOL,
    }

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context.update(kwargs)
        return context


class CustomPasswordResetDoneView(PasswordResetDoneView):
    title = _("Password reset sent, please check your email")


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    """
    A custom password reset confirm view that extends Django's built-in PasswordResetView.
    """

    success_url = reverse_lazy("accounts:custom_password_reset_complete")



class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    """
    A custom password reset complete view that extends Django's built-in PasswordResetView.
    """

    title = _("Password reset completed successfully")







