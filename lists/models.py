from django.conf import settings
from django.db import models

from movies.models import Movie


class List(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="lists",
    )

    name = models.CharField(max_length=100)

    description = models.TextField(blank=True)

    is_public = models.BooleanField(default=True)

    is_watchlist = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "name"],
                name="unique_user_list",
            )
        ]

    def __str__(self):
        return self.name


class ListItem(models.Model):
    movie_list = models.ForeignKey(
        List,
        on_delete=models.CASCADE,
        related_name="items",
    )

    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        related_name="list_items",
    )

    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["movie_list", "movie"],
                name="unique_movie_in_list",
            )
        ]

    def __str__(self):
        return f"{self.movie.title} ({self.movie_list.name})"
