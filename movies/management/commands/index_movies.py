from django.core.management.base import BaseCommand

from movies.models import Movie
from movies.search import es


class Command(BaseCommand):
    help = "Index all movies into Elasticsearch"

    def handle(self, *args, **options):

        if es.indices.exists(index="movies"):
            es.indices.delete(index="movies")

        es.indices.create(
            index="movies",
            mappings={
                "properties": {
                    "title": {"type": "text"},
                    "original_title": {"type": "text"},
                    "overview": {"type": "text"},
                    "tagline": {"type": "text"},
                    "vote_average": {"type": "float"},
                    "vote_count": {"type": "integer"},
                    "popularity": {"type": "float"},
                    "release_date": {"type": "date"},
                    "original_language": {"type": "keyword"},
                }
            },
        )

        for movie in Movie.objects.all():
            es.index(
                index="movies",
                id=movie.id,
                document={
                    "title": movie.title,
                    "original_title": movie.original_title,
                    "overview": movie.overview,
                    "tagline": movie.tagline,
                    "vote_average": movie.vote_average,
                    "vote_count": movie.vote_count,
                    "popularity": movie.popularity,
                    "release_date": (
                        movie.release_date.isoformat() if movie.release_date else None
                    ),
                    "original_language": movie.original_language,
                },
            )

            self.stdout.write(self.style.SUCCESS(movie.title))

        self.stdout.write(self.style.SUCCESS("Movies indexed successfully."))
