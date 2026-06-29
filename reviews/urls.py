from django.urls import path

from .views import (
    DeleteReviewView,
    RateMovieView,
    RemoveRatingView,
    ReviewView,
    UserRatingsView,
    UserReviewsView,
    VoteReviewView,
)

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
    path(
        "movies/<int:pk>/review/",
        ReviewView.as_view(),
        name="review_movie",
    ),
    path(
        "movies/<int:pk>/review/delete/",
        DeleteReviewView.as_view(),
        name="delete_review",
    ),
    path(
        "reviews/<int:pk>/vote/",
        VoteReviewView.as_view(),
        name="vote_review",
    ),
    path(
        "ratings/",
        UserRatingsView.as_view(),
        name="user_ratings",
    ),
    path(
        "reviews/",
        UserReviewsView.as_view(),
        name="user_reviews",
    ),
]
