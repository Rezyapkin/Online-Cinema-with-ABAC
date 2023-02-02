from django.urls import path, include


urlpatterns = [
    path("v1/", include("server.apps.movies.api.v1.urls")),
]
