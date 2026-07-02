from reviews.models import MovieRating, Review


def update_popularity(movie):

    rating_count = MovieRating.objects.filter(
        movie=movie,
    ).count()

    review_count = Review.objects.filter(
        movie=movie,
    ).count()

    movie.popularity = rating_count + (review_count * 2)

    movie.save(update_fields=["popularity"])
