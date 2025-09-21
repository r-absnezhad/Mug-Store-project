from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from mail_templated import EmailMessage
from django.utils.translation import gettext_lazy as _
from rest_framework.response import Response
from ..serializers import (
    RegistrationSerializer,
    CustomAuthTokenSerializer,
    CustomTokenObtainPairSerializer,
    ActivationResendSerializer,
)
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from ...utils import EmailThread
from django.contrib.auth import get_user_model
User = get_user_model()
from django.urls import reverse_lazy
import jwt
from django.conf import settings
from django.conf import settings
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError




class RegistrationApiView(generics.GenericAPIView):
    """
    API view for user registration.
    Handles user sign-up, generates an activation token, and sends an activation email.
    """
    serializer_class = RegistrationSerializer


    def post(self, request, *args, **kwargs):
        """
        Handle POST requests for user registration.
        - Validates the registration data using the serializer.
        - Creates a new user if the data is valid.
        - Generates an activation token for the user.
        - Sends an activation email to the user with the token.
        """
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            email = serializer.validated_data["email"]
            data = {
                "email": email,
            }
            user_obj = get_object_or_404(User, email=email)
            token = self.get_tokens_for_user(user_obj)
            email_obj = EmailMessage(
                "email/activation_email.tpl",
                {"token": token},
                "reihaneabbasnezhadsarab@gmail.com",
                to=[email],
            )
            EmailThread(email_obj).start()
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)
    



class ActivationApiView(APIView):
    def get(self, request, token, *args, **kwargs):
        try:
            token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = token.get("user_id")
        except ExpiredSignatureError:
            return Response({'details':'token has been expired'}, status=status.HTTP_400_BAD_REQUEST)
        except InvalidSignatureError:
            return Response({'details':'token is not valid '}, status=status.HTTP_400_BAD_REQUEST)
        user_obj = User.objects.get(pk=user_id) 
        if user_obj.is_verified:
            return Response({'details':'Your account has already been activated '}, status=status.HTTP_200_OK)
        user_obj.is_verified = True
        user_obj.save()
        return Response({'details':'Your account has been verified and activated successfully'}, status=status.HTTP_200_OK)



class ActivationResendApiView(generics.GenericAPIView):
    serializer_class = ActivationResendSerializer
    def post(self, request, *args, **kwargs):
        serializer = ActivationResendSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_obj = serializer.validated_data["user"]
        email = serializer.validated_data["email"]
        if email:
            token = self.get_tokens_for_user(user_obj)
            email_obj = EmailMessage(
                "email/activation_email.tpl",
                {"token": token},
                "reihaneabbasnezhadsarab@gmail.com",
                to=[email],
            )
            EmailThread(email_obj).start()
            return Response({'details':'activation resend successfully'}, status=status.HTTP_200_OK)
            
        else:
            return Response({'details':'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)




class CustomObtainAuthToken(ObtainAuthToken):
    """
    Custom view for user authentication using token-based authentication.
    Extends the default `ObtainAuthToken` to return additional user details along with the token.
    """
    serializer_class = CustomAuthTokenSerializer
    def post(self, request, *args, **kwargs):
        """
        Handle POST requests for user authentication.
        - Validates the user credentials using the custom serializer.
        - If valid, generates or retrieves an authentication token for the user.
        - Returns the token along with additional user details (user ID, email, username).
        """
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        # send access_token
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "token": str(refresh.access_token),
                "user_id": user.pk,
                "email": user.email,
                "username": user.username,
            }
        )



class CustomDiscardAuthToken(APIView):
    """
    API view for discarding (logging out) the authentication token.
    Allows authenticated users to manually invalidate their token by deleting it.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom view for obtaining JWT access and refresh tokens.
    """

    serializer_class = CustomTokenObtainPairSerializer
