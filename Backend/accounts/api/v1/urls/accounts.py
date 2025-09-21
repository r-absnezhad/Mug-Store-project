from django.urls import path, include
from .. import views
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)


router = SimpleRouter()
router.register(r'users', views.UserModelViewSet, basename="users")

urlpatterns = [
    path('', include(router.urls)),
    # registration / sign up
    path("registration/", views.RegistrationApiView.as_view(), name="registration"),
    # activation
    path("activation/confirm/<str:token>", views.ActivationApiView.as_view(), name ="activation"),
    # resend activation
    path("activation/resend/", views.ActivationResendApiView.as_view(), name ="activation-resend"),

    # login 
    path("token/login/", views.CustomObtainAuthToken.as_view(), name="token-login"),
    # logout
    path("token/logout/", views.CustomDiscardAuthToken.as_view(), name="token-logout"),
    #  jwt authentication
    path('jwt/token/create/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('jwt/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('jwt/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # change password
    path(
        "change_password/",
        views.CustomChangePasswordApiView.as_view(),
        name="change-password",
    ),
    # reset password
    # reset password confirmation
    path(
        "password_reset/",
        views.CustomPasswordResetView.as_view(),
        name="custom_password_reset",
    ),
    path(
        "password_reset_done/",
        views.CustomPasswordResetDoneView.as_view(
            template_name="registration/password_reset_done.html"
        ),
        name="custom_password_reset_done",
    ),
    path(
        "password_reset_confirm/<uidb64>/<token>/",
        views.CustomPasswordResetConfirmView.as_view(
            template_name="registration/password_reset_confirm.html"
        ),
        name="custom_password_reset_confirm",
    ),
    path(
        "password_reset_complete/",
        views.CustomPasswordResetCompleteView.as_view(
            template_name="registration/password_reset_complete.html"
        ),
        name="custom_password_reset_complete",
    ),  

]
urlpatterns += router.urls