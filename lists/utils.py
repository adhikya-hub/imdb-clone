from .models import List, ListItem


def add_to_history(user, movie):
    history, created = List.objects.get_or_create(
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
