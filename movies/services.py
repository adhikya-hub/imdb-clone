import requests
from django.conf import settings

BASE_URL = "https://api.themoviedb.org/3"


def get_popular_movies(page=1):
    response = requests.get(
        f"{BASE_URL}/movie/popular",
        params={
            "api_key": settings.TMDB_API_KEY,
            "page": page,
        },
    )

    response.raise_for_status()
    return response.json()


# def get_popular_movies(page=1):
#     print("API Key:", settings.TMDB_API_KEY[:5])

#     response = requests.get(
#         f"{BASE_URL}/movie/popular",
#         params={
#             "api_key": settings.TMDB_API_KEY,
#             "page": page,
#         },
#         timeout=10,
#     )

#     print(response.status_code)

#     response.raise_for_status()
#     return response.json()


def get_movie_details(movie_id):
    response = requests.get(
        f"{BASE_URL}/movie/{movie_id}",
        params={
            "api_key": settings.TMDB_API_KEY,
        },
    )

    response.raise_for_status()
    return response.json()


def get_movie_credits(movie_id):
    response = requests.get(
        f"{BASE_URL}/movie/{movie_id}/credits",
        params={
            "api_key": settings.TMDB_API_KEY,
        },
    )

    response.raise_for_status()
    return response.json()


def get_person_details(person_id):
    response = requests.get(
        f"{BASE_URL}/person/{person_id}",
        params={
            "api_key": settings.TMDB_API_KEY,
        },
    )

    response.raise_for_status()
    return response.json()
