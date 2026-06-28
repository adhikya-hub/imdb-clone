from django.urls import path

from .views import RateMovieView

urlpatterns = [
    path(
        "movies/<int:pk>/rate/",
        RateMovieView.as_view(),
        name="rate_movie",
    ),
]
