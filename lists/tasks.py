import csv
from pathlib import Path

from celery import shared_task
from django.conf import settings

from .models import List


@shared_task
def export_list_csv(list_id):

    movie_list = List.objects.get(pk=list_id)

    export_dir = Path(settings.MEDIA_ROOT) / "exports"
    export_dir.mkdir(parents=True, exist_ok=True)

    filename = f"list_{movie_list.id}.csv"
    filepath = export_dir / filename

    with open(filepath, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow(
            [
                "Title",
                "Release Year",
                "IMDb Rating",
                "Your Rating",
                "Runtime",
            ]
        )

        for item in movie_list.items.select_related("movie"):
            movie = item.movie

            writer.writerow(
                [
                    movie.title,
                    movie.release_date.year if movie.release_date else "",
                    movie.vote_average,
                    "",
                    movie.runtime,
                ]
            )

    return f"exports/{filename}"
