from django.urls import path

from .views import HomeView, MovieDetailView, PersonDetailView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("movies/<int:pk>/", MovieDetailView.as_view(), name="movie_detail"),
    path("people/<int:pk>/", PersonDetailView.as_view(), name="person_detail"),
]
