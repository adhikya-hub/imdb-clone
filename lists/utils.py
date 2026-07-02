from lists.models import FavoritePerson, List, ListItem
from reviews.models import MovieRating, Review


def add_to_history(user, movie):
    history, _ = List.objects.get_or_create(
        user=user,
        is_history=True,
        defaults={
            "name": "Watch History",
            "description": "",
            "is_public": False,
        },
    )

    ListItem.objects.get_or_create(
        movie_list=history,
        movie=movie,
    )

    watchlist = List.objects.filter(
        user=user,
        is_watchlist=True,
    ).first()

    if watchlist:
        ListItem.objects.filter(
            movie_list=watchlist,
            movie=movie,
        ).delete()


def remove_from_history(user, movie):
    history = List.objects.filter(
        user=user,
        is_history=True,
    ).first()

    if history:
        ListItem.objects.filter(
            movie_list=history,
            movie=movie,
        ).delete()


def annotate_movies(user, items):

    history = List.objects.filter(
        user=user,
        is_history=True,
    ).first()

    history_ids = set()

    if history:
        history_ids = set(history.items.values_list("movie_id", flat=True))

    watchlist = List.objects.filter(
        user=user,
        is_watchlist=True,
    ).first()

    watchlist_ids = set()

    if watchlist:
        watchlist_ids = set(watchlist.items.values_list("movie_id", flat=True))

    ratings = {
        rating.movie_id: rating.rating
        for rating in MovieRating.objects.filter(user=user)
    }

    reviews = set(
        Review.objects.filter(user=user).values_list(
            "movie_id",
            flat=True,
        )
    )

    for item in items:
        movie = item.movie

        movie.user_rating = ratings.get(movie.id)

        movie.user_review = movie.id in reviews

        movie.in_watchlist = movie.id in watchlist_ids

        movie.in_history = (
            movie.id in history_ids
            or movie.user_rating is not None
            or movie.user_review
        )


def add_sidebar_previews(user, context):

    watchlist = List.objects.filter(
        user=user,
        is_watchlist=True,
    ).first()

    history = List.objects.filter(
        user=user,
        is_history=True,
    ).first()

    latest_rating = (
        MovieRating.objects.filter(user=user)
        .select_related("movie")
        .order_by("-updated_at")
        .first()
    )

    latest_favorite = (
        FavoritePerson.objects.filter(user=user)
        .select_related("person")
        .order_by("-created_at")
        .first()
    )

    context["watchlist_preview"] = None
    context["history_preview"] = None
    context["ratings_preview"] = None
    context["favorite_people_preview"] = None

    if watchlist and watchlist.items.exists():
        context["watchlist_preview"] = watchlist.items.first().movie.poster_path

    if history and history.items.exists():
        context["history_preview"] = history.items.first().movie.poster_path

    if latest_rating:
        context["ratings_preview"] = latest_rating.movie.poster_path

    if latest_favorite:
        context["favorite_people_preview"] = latest_favorite.person.profile_path
