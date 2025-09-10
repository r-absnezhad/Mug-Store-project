from django.urls import path, include

urlpatterns = [
    path("api/v1/", include("customizers.api.v1.urls")),
]