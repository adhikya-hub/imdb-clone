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


class Review(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reviews",
    )

    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        related_name="reviews",
    )

    title = models.CharField(max_length=100)

    body = models.TextField()

    spoiler = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "movie"],
                name="unique_review",
            )
        ]

    def __str__(self):
        return f"{self.user} - {self.movie}"


class ReviewVote(models.Model):
    HELPFUL = 1
    NOT_HELPFUL = -1

    CHOICES = (
        (HELPFUL, "Helpful"),
        (NOT_HELPFUL, "Not Helpful"),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="review_votes",
    )

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name="votes",
    )

    value = models.SmallIntegerField(choices=CHOICES)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "review"],
                name="unique_review_vote",
            )
        ]

    def __str__(self):
        return f"{self.user} - {self.review}"
