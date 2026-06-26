import ssl

import httpx
from django.conf import settings

BASE_URL = "https://api.themoviedb.org/3"
IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"

ssl_ctx = ssl.create_default_context()
ssl_ctx.minimum_version = ssl.TLSVersion.TLSv1_2
ssl_ctx.set_ciphers("DEFAULT@SECLEVEL=1")

client = httpx.Client(verify=ssl_ctx)

headers = {
    "Authorization": f"Bearer {settings.TMDB_ACCESS_TOKEN}",
    "User-Agent": "Mozilla/5.0",
}


def get_popular_movies(page=1):
    response = client.get(
        f"{BASE_URL}/movie/popular",
        params={"page": page},
        headers=headers,
    )
    response.raise_for_status()
    return response.json()


def get_movie_details(movie_id):
    response = client.get(
        f"{BASE_URL}/movie/{movie_id}",
        headers=headers,
    )
    response.raise_for_status()
    return response.json()


def get_movie_credits(movie_id):
    response = client.get(
        f"{BASE_URL}/movie/{movie_id}/credits",
        headers=headers,
    )
    response.raise_for_status()
    return response.json()


def get_person_details(person_id):
    response = client.get(
        f"{BASE_URL}/person/{person_id}",
        headers=headers,
    )
    response.raise_for_status()
    return response.json()


def get_movie_videos(movie_id):
    response = client.get(
        f"{BASE_URL}/movie/{movie_id}/videos",
        headers=headers,
    )
    response.raise_for_status()
    return response.json()
