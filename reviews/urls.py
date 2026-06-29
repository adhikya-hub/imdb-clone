from django.urls import path

from .views import RateMovieView, RemoveRatingView

urlpatterns = [
    path(
        "movies/<int:pk>/rate/",
        RateMovieView.as_view(),
        name="rate_movie",
    ),
    path(
        "movies/<int:pk>/remove-rating/",
        RemoveRatingView.as_view(),
        name="remove_rating",
    ),
]
