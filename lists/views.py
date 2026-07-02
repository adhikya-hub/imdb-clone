from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from lists.utils import add_to_history, annotate_movies, remove_from_history
from movies.models import Movie, Person
from reviews.models import MovieRating, Review

from .forms import ListForm
from .models import FavoritePerson, List, ListItem


class ToggleWatchlistView(LoginRequiredMixin, View):
    def post(self, request, pk):

        movie = get_object_or_404(Movie, pk=pk)

        watchlist, _ = List.objects.get_or_create(
            user=request.user,
            is_watchlist=True,
            defaults={
                "name": "Watchlist",
                "description": "",
            },
        )

        item = ListItem.objects.filter(
            movie_list=watchlist,
            movie=movie,
        )

        if item.exists():
            item.delete()

            in_watchlist = False

        else:
            ListItem.objects.create(
                movie_list=watchlist,
                movie=movie,
            )

            in_watchlist = True

        return JsonResponse(
            {
                "watchlist": in_watchlist,
            }
        )


class WatchlistView(LoginRequiredMixin, ListView):
    model = ListItem
    template_name = "lists/watchlist.html"
    context_object_name = "items"

    def get_queryset(self):

        watchlist, created = List.objects.get_or_create(
            user=self.request.user,
            is_watchlist=True,
            defaults={
                "name": "Watchlist",
                "description": "My Watchlist",
                "is_public": False,
            },
        )

        items = list(watchlist.items.select_related("movie").order_by("-added_at"))

        annotate_movies(self.request.user, items)

        return items

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["preview_image"] = None

        if context["items"]:
            context["preview_image"] = context["items"][0].movie.poster_path

        return context


class UserListsView(LoginRequiredMixin, ListView):
    model = List
    template_name = "lists/list_list.html"
    context_object_name = "lists"

    def get_queryset(self):
        return List.objects.filter(
            user=self.request.user,
            is_watchlist=False,
            is_history=False,
        ).order_by("-updated_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        watchlist = List.objects.filter(
            user=self.request.user,
            is_watchlist=True,
        ).first()

        if watchlist:
            context["watchlist_count"] = watchlist.items.count()
        else:
            context["watchlist_count"] = 0

        context["page_title"] = "Your Lists"
        context["page_description"] = "Lists you've created."

        return context


class ListDetailView(LoginRequiredMixin, DetailView):
    model = List
    template_name = "lists/list_detail.html"
    context_object_name = "movie_list"

    def get_queryset(self):
        return List.objects.filter(user=self.request.user).prefetch_related(
            "items__movie"
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        items = list(context["movie_list"].items.select_related("movie"))

        annotate_movies(self.request.user, items)

        context["items"] = items

        return context


class RemoveListItemView(LoginRequiredMixin, View):
    def post(self, request, list_id, movie_id):

        item = get_object_or_404(
            ListItem,
            movie_list__id=list_id,
            movie_list__user=request.user,
            movie_id=movie_id,
        )

        item.delete()

        return redirect("list_detail", pk=list_id)


class CreateListView(LoginRequiredMixin, CreateView):
    model = List
    form_class = ListForm
    template_name = "lists/list_form.html"
    success_url = reverse_lazy("lists")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class UpdateListView(LoginRequiredMixin, UpdateView):
    model = List
    form_class = ListForm
    template_name = "lists/list_form.html"
    success_url = reverse_lazy("lists")

    def get_queryset(self):
        return List.objects.filter(user=self.request.user)


class DeleteListView(LoginRequiredMixin, DeleteView):
    model = List
    success_url = reverse_lazy("lists")
    template_name = "lists/delete_list.html"

    def get_queryset(self):
        return List.objects.filter(user=self.request.user)


class UpdateMovieListsView(LoginRequiredMixin, View):
    def post(self, request, pk):

        movie = get_object_or_404(Movie, pk=pk)

        selected_lists = request.POST.getlist("lists")

        user_lists = List.objects.filter(
            user=request.user,
            is_watchlist=False,
            is_history=False,
        )

        saved_to = 0

        for movie_list in user_lists:
            if str(movie_list.id) in selected_lists:
                ListItem.objects.get_or_create(
                    movie_list=movie_list,
                    movie=movie,
                )

                saved_to += 1

            else:
                ListItem.objects.filter(
                    movie_list=movie_list,
                    movie=movie,
                ).delete()

        return JsonResponse(
            {
                "success": True,
                "saved_to": saved_to,
            }
        )


class HistoryView(LoginRequiredMixin, ListView):
    model = ListItem
    template_name = "lists/history.html"
    context_object_name = "items"

    def get_queryset(self):

        history, created = List.objects.get_or_create(
            user=self.request.user,
            is_history=True,
            defaults={
                "name": "Watch History",
                "description": "",
                "is_public": False,
            },
        )

        items = list(history.items.select_related("movie").order_by("-added_at"))

        annotate_movies(self.request.user, items)

        return items

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["preview_image"] = None

        if context["items"]:
            context["preview_image"] = context["items"][0].movie.poster_path

        return context


class ToggleHistoryView(LoginRequiredMixin, View):
    def post(self, request, pk):

        movie = get_object_or_404(Movie, pk=pk)

        history = List.objects.filter(
            user=request.user,
            is_history=True,
        ).first()

        in_history = (
            history
            and ListItem.objects.filter(
                movie_list=history,
                movie=movie,
            ).exists()
        )

        has_rating = MovieRating.objects.filter(
            user=request.user,
            movie=movie,
        ).exists()

        has_review = Review.objects.filter(
            user=request.user,
            movie=movie,
        ).exists()

        if in_history:
            if has_rating or has_review:
                return JsonResponse(
                    {
                        "watched": True,
                        "message": "To remove this from your watch history, remove your rating or review first.",
                    }
                )

            remove_from_history(request.user, movie)

            return JsonResponse(
                {
                    "watched": False,
                }
            )

        add_to_history(request.user, movie)

        return JsonResponse(
            {
                "watched": True,
            }
        )


class RemoveHistoryView(LoginRequiredMixin, View):
    def post(self, request, pk):

        movie = get_object_or_404(Movie, pk=pk)

        history = get_object_or_404(
            List,
            user=request.user,
            is_history=True,
        )

        has_rating = MovieRating.objects.filter(
            user=request.user,
            movie=movie,
        ).exists()

        has_review = Review.objects.filter(
            user=request.user,
            movie=movie,
        ).exists()

        if has_rating or has_review:
            messages.error(
                request,
                "To remove this movie from your Watch History, remove your rating and review first.",
            )

            return redirect("history")

        ListItem.objects.filter(
            movie_list=history,
            movie=movie,
        ).delete()

        messages.success(
            request,
            "Movie removed from Watch History.",
        )

        return redirect("history")


class ToggleFavoritePersonView(LoginRequiredMixin, View):
    def post(self, request, pk):

        person = get_object_or_404(Person, pk=pk)

        favorite, created = FavoritePerson.objects.get_or_create(
            user=request.user,
            person=person,
        )

        if not created:
            favorite.delete()
            is_favorite = False
        else:
            is_favorite = True

        return JsonResponse(
            {
                "favorite": is_favorite,
            }
        )


class FavoritePeopleView(LoginRequiredMixin, ListView):
    model = FavoritePerson
    template_name = "lists/favorite_people.html"
    context_object_name = "favorites"

    def get_queryset(self):
        return (
            FavoritePerson.objects.filter(user=self.request.user)
            .select_related("person")
            .order_by("-created_at")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["preview_image"] = None

        if context["favorites"]:
            context["preview_image"] = context["favorites"][0].person.profile_path

        return context
