from django.views.generic import DetailView, ListView

from reviews.forms import MovieRatingForm
from reviews.models import MovieRating

from .models import Movie, Person


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        youtube_videos = [
            video for video in self.object.videos if video["site"] == "YouTube"
        ]

        context["videos"] = youtube_videos
        context["featured_video"] = youtube_videos[0] if youtube_videos else None

        context["cast"] = (
            self.object.credits.filter(job="Actor")
            .select_related("person")
            .order_by("cast_order")
        )

        context["crew"] = self.object.credits.exclude(job="Actor").select_related(
            "person"
        )

        if self.request.user.is_authenticated:
            user_rating = MovieRating.objects.filter(
                movie=self.object,
                user=self.request.user,
            ).first()

            context["user_rating"] = user_rating
            context["rating_form"] = MovieRatingForm(instance=user_rating)
        else:
            context["user_rating"] = None
            context["rating_form"] = MovieRatingForm()

        context["ratings"] = range(1, 11)

        return context


class PersonDetailView(DetailView):
    model = Person
    template_name = "movies/person_detail.html"
    context_object_name = "person"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["filmography"] = self.object.credits.select_related("movie").order_by(
            "-movie__release_date"
        )

        return context
