from django.urls import path
from .. import views


urlpatterns = [
    # check profile to have phone number
    path("check/", views.CheckProfileApiView.as_view(), name="check-profile"),
    # update phone number and information of a single profile 
    path("update/", views.ProfileRetrieveUpdateAPIView.as_view(), name="profile-retrieve-update"),
    # a list of all profiles.
    path("", views.ProfileListApiView.as_view(), name="profile-list"),

]
