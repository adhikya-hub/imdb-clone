from django.conf import settings
from django.db import models

from movies.models import Movie


class MovieRating(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="ratings",
    )

    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        related_name="ratings",
    )

    rating = models.PositiveSmallIntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "movie"],
                name="unique_movie_rating",
            )
        ]

    def __str__(self):
        return f"{self.user.username} rated {self.movie.title} {self.rating}/10"
