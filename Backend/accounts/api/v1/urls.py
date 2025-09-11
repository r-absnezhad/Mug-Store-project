from django.urls import path, include
from .views import ProfileModelViewSet, UserModelViewSet

from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register(r'users', UserModelViewSet)
router.register(r'profiles', ProfileModelViewSet)

urlpatterns = [
    path('', include(router.urls)),

    # registration
    # log in
    # log out
    # password change
    # password reset
    # password reset confirmation
    # email verification 
    # resend email verification    

]