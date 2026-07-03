from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    is_imdb_pro = models.BooleanField(default=False)

    profile_picture = models.ImageField(
        upload_to="profile_pictures/",
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.username
