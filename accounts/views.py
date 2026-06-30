from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from lists.models import FavoritePerson, List
from reviews.models import MovieRating, Review

from .forms import SignUpForm


class LoginLandingView(TemplateView):
    template_name = "registration/login.html"


class SignInView(LoginView):
    template_name = "registration/signin.html"


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user

        watchlist = List.objects.filter(
            user=user,
            is_watchlist=True,
        ).first()

        history = List.objects.filter(
            user=user,
            is_history=True,
        ).first()

        context["ratings"] = (
            MovieRating.objects.filter(user=user)
            .select_related("movie")
            .order_by("-updated_at")[:8]
        )

        context["reviews"] = (
            Review.objects.filter(user=user)
            .select_related("movie")
            .order_by("-updated_at")[:4]
        )

        context["watchlist"] = (
            watchlist.items.select_related("movie")[:8] if watchlist else []
        )

        context["history"] = (
            history.items.select_related("movie")[:8] if history else []
        )

        context["lists"] = List.objects.filter(
            user=user,
            is_watchlist=False,
            is_history=False,
        )[:5]

        context["favorite_people"] = (
            FavoritePerson.objects.filter(user=user)
            .select_related("person")
            .order_by("-created_at")[:8]
        )

        context["rating_count"] = MovieRating.objects.filter(user=user).count()

        context["review_count"] = Review.objects.filter(user=user).count()

        context["watchlist_count"] = watchlist.items.count() if watchlist else 0

        context["history_count"] = history.items.count() if history else 0

        context["list_count"] = List.objects.filter(
            user=user,
            is_watchlist=False,
            is_history=False,
        ).count()

        context["favorite_people_count"] = FavoritePerson.objects.filter(
            user=user
        ).count()

        return context
