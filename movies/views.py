from django.db.models import Count, Q
from django.views.generic import DetailView, ListView

from lists.models import FavoritePerson, List, ListItem
from reviews.forms import MovieRatingForm, ReviewForm
from reviews.models import MovieRating, Review, ReviewVote

from .models import Movie, Person
from .search import es


class HomeView(ListView):
    model = Movie
    template_name = "movies/home.html"
    context_object_name = "movies"
    paginate_by = 20

    def get_queryset(self):
        query = self.request.GET.get("q")

        if query:
            response = es.search(
                index="movies",
                query={
                    "multi_match": {
                        "query": query,
                        "fields": [
                            "title^3",
                            "original_title^2",
                            "overview",
                            "tagline",
                        ],
                        "fuzziness": "AUTO",
                    }
                },
            )

            ids = [int(hit["_id"]) for hit in response["hits"]["hits"]]

            movies = {movie.id: movie for movie in Movie.objects.filter(id__in=ids)}

            return [movies[id] for id in ids if id in movies]

        return Movie.objects.order_by("popularity")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            context["watchlist_ids"] = set(
                ListItem.objects.filter(
                    movie_list__user=self.request.user,
                    movie_list__is_watchlist=True,
                ).values_list("movie_id", flat=True)
            )
        else:
            context["watchlist_ids"] = set()

        context["search_query"] = self.request.GET.get("q", "")

        context["people"] = Person.objects.order_by("-popularity")[:12]

        if self.request.user.is_authenticated:
            context["favorite_people"] = set(
                FavoritePerson.objects.filter(
                    user=self.request.user,
                ).values_list(
                    "person_id",
                    flat=True,
                )
            )
        else:
            context["favorite_people"] = set()

        return context


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

        reviews = self.object.reviews.select_related("user").order_by("-created_at")

        ratings = {
            rating.user_id: rating.rating
            for rating in MovieRating.objects.filter(movie=self.object)
        }

        for review in reviews:
            review.user_rating = ratings.get(review.user_id)

        reviews = reviews.annotate(
            helpful_count=Count(
                "votes",
                filter=Q(votes__value=1),
            ),
            not_helpful_count=Count(
                "votes",
                filter=Q(votes__value=-1),
            ),
        )

        if self.request.user.is_authenticated:
            user_votes = {
                vote.review_id: vote.value
                for vote in ReviewVote.objects.filter(
                    user=self.request.user,
                    review__movie=self.object,
                )
            }

            for review in reviews:
                review.user_vote = user_votes.get(review.id)

        else:
            for review in reviews:
                review.user_vote = None

        context["reviews"] = reviews

        if self.request.user.is_authenticated:
            user_review = Review.objects.filter(
                movie=self.object,
                user=self.request.user,
            ).first()

            context["review_form"] = ReviewForm(instance=user_review)

            context["user_review"] = user_review

        else:
            context["review_form"] = ReviewForm()

        if self.request.user.is_authenticated:
            context["in_watchlist"] = ListItem.objects.filter(
                movie=self.object,
                movie_list__user=self.request.user,
                movie_list__is_watchlist=True,
            ).exists()
        else:
            context["in_watchlist"] = False

        if self.request.user.is_authenticated:
            context["lists"] = List.objects.filter(
                user=self.request.user,
                is_watchlist=False,
                is_history=False,
            )

            context["selected_lists"] = list(
                List.objects.filter(
                    user=self.request.user,
                    is_watchlist=False,
                    is_history=False,
                    items__movie=self.object,
                ).values_list("id", flat=True)
            )

        else:
            context["lists"] = []
            context["selected_lists"] = []

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
        if self.request.user.is_authenticated:
            context["is_favorite"] = FavoritePerson.objects.filter(
                user=self.request.user,
                person=self.object,
            ).exists()

        else:
            context["is_favorite"] = False

        return context


# class HomeView(ListView):
#     model = Movie
#     template_name = "movies/home.html"
#     context_object_name = "movies"
#     ordering = ["-popularity"]
#     paginate_by = 20

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)

#         if self.request.user.is_authenticated:
#             context["watchlist_ids"] = set(
#                 ListItem.objects.filter(
#                     movie_list__user=self.request.user,
#                     movie_list__is_watchlist=True,
#                 ).values_list(
#                     "movie_id",
#                     flat=True,
#                 )
#             )

#         else:
#             context["watchlist_ids"] = set()

#         return context
