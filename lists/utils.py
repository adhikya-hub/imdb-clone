from collections import Counter

from lists.models import FavoritePerson, List, ListItem
from movies.models import Genre
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


def sort_movies(items, sort):

    if sort == "recent":
        items.sort(
            key=lambda item: (
                item.added_at if hasattr(item, "added_at") else item.updated_at
            ),
            reverse=True,
        )

    elif sort == "alphabetical":
        items.sort(
            key=lambda item: item.movie.title.lower(),
        )

    elif sort == "imdb_rating":
        items.sort(
            key=lambda item: item.movie.vote_average,
            reverse=True,
        )

    elif sort == "popularity":
        items.sort(
            key=lambda item: item.movie.popularity,
            reverse=True,
        )

    elif sort == "ratings":
        items.sort(
            key=lambda item: item.movie.vote_count,
            reverse=True,
        )

    elif sort == "release":
        items.sort(
            key=lambda item: item.movie.release_date or "",
            reverse=True,
        )

    elif sort == "runtime":
        items.sort(
            key=lambda item: item.movie.runtime or 0,
            reverse=True,
        )

    elif sort == "your_rating":
        items.sort(
            key=lambda item: item.movie.user_rating or 0,
            reverse=True,
        )

    return items


def add_filter_data(request, context, items):

    counter = Counter()

    for item in items:
        for genre in item.movie.genres.all():
            counter[genre] += 1

    context["genres"] = sorted(
        counter.items(),
        key=lambda genre: genre[0].name,
    )

    context["selected_genres"] = request.GET.getlist("genre")

    context["year_from"] = request.GET.get("year_from", "")
    context["year_to"] = request.GET.get("year_to", "")

    context["imdb_from"] = request.GET.get("imdb_from", "")
    context["imdb_to"] = request.GET.get("imdb_to", "")

    context["user_from"] = request.GET.get("user_from", "")
    context["user_to"] = request.GET.get("user_to", "")

    return context


def filter_movies(items, request):

    genre_ids = request.GET.getlist("genre")

    year_from = request.GET.get("year_from")

    year_to = request.GET.get("year_to")

    imdb_from = request.GET.get("imdb_from")

    imdb_to = request.GET.get("imdb_to")

    user_from = request.GET.get("user_from")

    user_to = request.GET.get("user_to")

    filtered = []

    for item in items:
        movie = item.movie

        if genre_ids:
            movie_genres = {str(genre.id) for genre in movie.genres.all()}

            if not movie_genres.intersection(genre_ids):
                continue

        if year_from:
            if not movie.release_date or movie.release_date.year < int(year_from):
                continue

        if year_to:
            if not movie.release_date or movie.release_date.year > int(year_to):
                continue

        if imdb_from:
            if movie.vote_average < float(imdb_from):
                continue

        if imdb_to:
            if movie.vote_average > float(imdb_to):
                continue

        if user_from:
            if movie.user_rating is None or movie.user_rating < int(user_from):
                continue

        if user_to:
            if movie.user_rating is None or movie.user_rating > int(user_to):
                continue

        filtered.append(item)

    return filtered
