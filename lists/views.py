from django.contrib.auth.mixins import LoginRequiredMixin
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
from django.views.generic.edit import CreateView

from movies.models import Movie

from .forms import ListForm
from .models import List, ListItem


class ToggleWatchlistView(LoginRequiredMixin, View):
    def post(self, request, pk):

        movie = get_object_or_404(Movie, pk=pk)

        watchlist, created = List.objects.get_or_create(
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
        else:
            ListItem.objects.create(
                movie_list=watchlist,
                movie=movie,
            )

        return redirect(request.META.get("HTTP_REFERER", "/"))


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

        return watchlist.items.select_related("movie").order_by("-added_at")


class UserListsView(LoginRequiredMixin, ListView):
    model = List
    template_name = "lists/list_list.html"
    context_object_name = "lists"

    def get_queryset(self):
        return List.objects.filter(
            user=self.request.user,
            is_watchlist=False,
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

        return context


class ListDetailView(LoginRequiredMixin, DetailView):
    model = List
    template_name = "lists/list_detail.html"
    context_object_name = "movie_list"

    def get_queryset(self):
        return List.objects.filter(user=self.request.user).prefetch_related(
            "items__movie"
        )


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

        user_lists = List.objects.filter(user=request.user)

        for movie_list in user_lists:
            if str(movie_list.id) in selected_lists:
                ListItem.objects.get_or_create(
                    movie_list=movie_list,
                    movie=movie,
                )

            else:
                ListItem.objects.filter(
                    movie_list=movie_list,
                    movie=movie,
                ).delete()

        return redirect("movie_detail", pk=pk)
