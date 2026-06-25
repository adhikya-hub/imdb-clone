import time

from django.core.management.base import BaseCommand

from movies.models import Person
from movies.services import IMAGE_BASE_URL, get_person_details


class Command(BaseCommand):
    help = "Import full person details from TMDB"

    def handle(self, *args, **kwargs):
        people = Person.objects.all()

        for person in people:
            details = get_person_details(person.id)

            Person.objects.update_or_create(
                id=person.id,
                defaults={
                    "name": details["name"],
                    "biography": details.get("biography") or "",
                    "birthday": details["birthday"] or None,
                    "deathday": details["deathday"] or None,
                    "gender": details["gender"],
                    "homepage": details.get("homepage") or "",
                    "imdb_id": details.get("imdb_id") or "",
                    "known_for_department": details["known_for_department"],
                    "place_of_birth": details.get("place_of_birth") or "",
                    "popularity": details["popularity"],
                    "profile_path": (
                        f"{IMAGE_BASE_URL}{details['profile_path']}"
                        if details["profile_path"]
                        else ""
                    ),
                    "also_known_as": details.get("also_known_as") or [],
                },
            )

            self.stdout.write(f"Imported: {person.name}")
            time.sleep(0.2)

        self.stdout.write(self.style.SUCCESS("People imported successfully."))
