from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView

from lists.utils import (
    add_sidebar_previews,
    add_to_history,
    annotate_movies,
    sort_movies,
)
from movies.models import Movie
from movies.utils import update_popularity

from .forms import ReviewForm
from .models import MovieRating, Review, ReviewVote


class RateMovieView(LoginRequiredMixin, View):
    def post(self, request, pk):

        movie = get_object_or_404(Movie, pk=pk)

        rating = int(request.POST.get("rating"))

        MovieRating.objects.update_or_create(
            user=request.user,
            movie=movie,
            defaults={
                "rating": rating,
            },
        )

        add_to_history(request.user, movie)

        movie.refresh_rating()
        update_popularity(movie)

        return JsonResponse(
            {
                "success": True,
                "rating": rating,
                "vote_average": movie.vote_average,
                "vote_count": movie.vote_count,
            }
        )


class RemoveRatingView(LoginRequiredMixin, View):
    def post(self, request, pk):
        movie = get_object_or_404(Movie, pk=pk)

        MovieRating.objects.filter(
            movie=movie,
            user=request.user,
        ).delete()

        movie.refresh_rating()

        return JsonResponse(
            {
                "removed": True,
                "vote_average": movie.vote_average,
                "vote_count": movie.vote_count,
            }
        )


class ReviewView(LoginRequiredMixin, View):
    def post(self, request, pk):

        movie = get_object_or_404(Movie, pk=pk)

        review = Review.objects.filter(
            movie=movie,
            user=request.user,
        ).first()

        form = ReviewForm(
            request.POST,
            instance=review,
        )

        if form.is_valid():
            review = form.save(commit=False)
            review.movie = movie
            review.user = request.user
            review.save()

            add_to_history(request.user, movie)
            update_popularity(movie)

        return redirect("movie_detail", pk=pk)


class DeleteReviewView(LoginRequiredMixin, View):
    def post(self, request, pk):

        movie = get_object_or_404(Movie, pk=pk)

        review = get_object_or_404(
            Review,
            movie=movie,
            user=request.user,
        )

        review.delete()

        return redirect("movie_detail", pk=pk)


class VoteReviewView(LoginRequiredMixin, View):
    def post(self, request, pk):

        review = get_object_or_404(Review, pk=pk)

        value = int(request.POST["value"])

        ReviewVote.objects.update_or_create(
            review=review,
            user=request.user,
            defaults={
                "value": value,
            },
        )

        helpful = review.votes.filter(value=ReviewVote.HELPFUL).count()
        not_helpful = review.votes.filter(value=ReviewVote.NOT_HELPFUL).count()

        return JsonResponse(
            {
                "success": True,
                "helpful": helpful,
                "not_helpful": not_helpful,
                "user_vote": value,
            }
        )


class UserRatingsView(LoginRequiredMixin, ListView):
    model = MovieRating
    template_name = "reviews/user_ratings.html"
    context_object_name = "ratings"

    def get_queryset(self):

        ratings = list(
            MovieRating.objects.filter(
                user=self.request.user,
            )
            .select_related("movie")
            .order_by("-updated_at")
        )

        annotate_movies(
            self.request.user,
            ratings,
        )

        return ratings

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        sort = self.request.GET.get(
            "sort",
            "recent",
        )

        context["ratings"] = sort_movies(
            list(context["ratings"]),
            sort,
        )

        context["current_sort"] = sort

        add_sidebar_previews(
            self.request.user,
            context,
        )

        return context


class UserReviewsView(LoginRequiredMixin, ListView):
    model = Review
    template_name = "reviews/user_reviews.html"
    context_object_name = "reviews"

    def get_queryset(self):
        return (
            Review.objects.filter(user=self.request.user)
            .select_related("movie")
            .order_by("-updated_at")
        )
