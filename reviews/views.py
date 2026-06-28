from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views import View

from movies.models import Movie

from .models import MovieRating


class RateMovieView(LoginRequiredMixin, View):
    def post(self, request, pk):

        movie = get_object_or_404(Movie, pk=pk)

        rating = request.POST.get("rating")

        MovieRating.objects.update_or_create(
            user=request.user,
            movie=movie,
            defaults={
                "rating": rating,
            },
        )

        return redirect("movie_detail", pk=pk)
