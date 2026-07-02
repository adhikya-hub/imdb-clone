from lists.models import List, ListItem
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
