from django.views.generic import DetailView, ListView

from .models import Movie


class HomeView(ListView):
    model = Movie
    template_name = "movies/home.html"
    context_object_name = "movies"
    ordering = ["-popularity"]
    paginate_by = 20


class MovieDetailView(DetailView):
    model = Movie
    template_name = "movies/movie_detail.html"
    context_object_name = "movie"

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)

    #     context["cast"] = self.object.credits.filter(job="Actor").order_by("cast_order")

    #     context["crew"] = self.object.credits.exclude(job="Actor")

    #     return context
