from django.core.management.base import BaseCommand

from movies.models import Credit, Genre, Movie, Person
from movies.services import (
    get_movie_credits,
    get_movie_details,
    get_person_details,
    get_popular_movies,
)


class Command(BaseCommand):
    help = "Import movies from TMDB"

    def handle(self, *args, **kwargs):
        data = get_popular_movies()

        for movie in data["results"]:
            details = get_movie_details(movie["id"])

            movie_obj, created = Movie.objects.update_or_create(
                id=details["id"],
                defaults={
                    "title": details["title"],
                    "original_title": details["original_title"],
                    "overview": details["overview"],
                    "tagline": details["tagline"],
                    "release_date": details["release_date"] or None,
                    "runtime": details["runtime"],
                    "status": details["status"],
                    "adult": details["adult"],
                    "homepage": details["homepage"],
                    "original_language": details["original_language"],
                    "popularity": details["popularity"],
                    "vote_average": details["vote_average"],
                    "vote_count": details["vote_count"],
                    "budget": details["budget"],
                    "revenue": details["revenue"],
                    "poster_path": details["poster_path"],
                    "backdrop_path": details["backdrop_path"],
                    "belongs_to_collection": details["belongs_to_collection"],
                    "origin_country": details["origin_country"],
                    "production_companies": details["production_companies"],
                    "production_countries": details["production_countries"],
                    "spoken_languages": details["spoken_languages"],
                },
            )
            for genre in details["genres"]:
                genre_obj, _ = Genre.objects.get_or_create(
                    id=genre["id"],
                    defaults={
                        "name": genre["name"],
                    },
                )

                movie_obj.genres.add(genre_obj)

            credits = get_movie_credits(movie_obj.id)

            for actor in credits["cast"]:
                person, _ = Person.objects.update_or_create(
                    id=actor["id"],
                    defaults={
                        "name": actor["name"],
                        "gender": actor["gender"],
                        "known_for_department": actor["known_for_department"],
                        "popularity": actor["popularity"],
                        "profile_path": actor["profile_path"],
                    },
                )

                Credit.objects.update_or_create(
                    credit_id=actor["credit_id"],
                    defaults={
                        "movie": movie_obj,
                        "person": person,
                        "department": "Acting",
                        "job": "Actor",
                        "character_name": actor["character"],
                        "cast_order": actor["order"],
                    },
                )
            for crew_member in credits["crew"]:
                person, _ = Person.objects.update_or_create(
                    id=crew_member["id"],
                    defaults={
                        "name": crew_member["name"],
                        "gender": crew_member["gender"],
                        "known_for_department": crew_member["known_for_department"],
                        "popularity": crew_member["popularity"],
                        "profile_path": crew_member["profile_path"],
                    },
                )

                Credit.objects.update_or_create(
                    credit_id=crew_member["credit_id"],
                    defaults={
                        "movie": movie_obj,
                        "person": person,
                        "department": crew_member["department"],
                        "job": crew_member["job"],
                        "character_name": "",
                        "cast_order": None,
                    },
                )
