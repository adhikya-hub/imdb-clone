from django.db import models
from django.db.models import Avg, Count


class Movie(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=255)
    original_title = models.CharField(max_length=255)
    overview = models.TextField()
    tagline = models.CharField(max_length=500, blank=True, null=True)
    release_date = models.DateField(null=True, blank=True)
    runtime = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=50, blank=True)
    adult = models.BooleanField(default=False)
    imdb_id = models.CharField(max_length=20, blank=True)
    homepage = models.URLField(blank=True, null=True)
    original_language = models.CharField(max_length=10, blank=True)
    popularity = models.FloatField(default=0)
    vote_average = models.FloatField(default=0)
    vote_count = models.IntegerField(default=0)
    budget = models.BigIntegerField(default=0)
    revenue = models.BigIntegerField(default=0)
    poster_path = models.CharField(max_length=255, blank=True, null=True)
    backdrop_path = models.CharField(max_length=255, blank=True, null=True)
    belongs_to_collection = models.JSONField(null=True, blank=True)
    origin_country = models.JSONField(default=list, blank=True)
    production_companies = models.JSONField(default=list, blank=True)
    production_countries = models.JSONField(default=list, blank=True)
    spoken_languages = models.JSONField(default=list, blank=True)
    videos = models.JSONField(default=list, blank=True)
    genres = models.ManyToManyField("Genre", related_name="movies")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def refresh_rating(self):
        stats = self.ratings.aggregate(
            average=Avg("rating"),
            count=Count("id"),
        )
        self.vote_average = round(stats["average"] or 0, 1)
        self.vote_count = stats["count"]
        self.save(update_fields=["vote_average", "vote_count"])

    def __str__(self):
        return self.title


class Genre(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Person(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    biography = models.TextField(blank=True)
    birthday = models.DateField(null=True, blank=True)
    deathday = models.DateField(null=True, blank=True)
    gender = models.IntegerField(null=True, blank=True)
    homepage = models.URLField(blank=True, null=True)
    imdb_id = models.CharField(max_length=20, blank=True, null=True)
    known_for_department = models.CharField(max_length=100, blank=True)
    place_of_birth = models.CharField(max_length=255, blank=True, null=True)
    popularity = models.FloatField(default=0)
    profile_path = models.CharField(max_length=255, blank=True, null=True)
    also_known_as = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Credit(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="credits")
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="credits")
    credit_id = models.CharField(max_length=50, unique=True)
    department = models.CharField(max_length=100, blank=True)
    job = models.CharField(max_length=100)
    character_name = models.CharField(max_length=255, blank=True, null=True)
    cast_order = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.person.name} - {self.job} ({self.movie.title})"
