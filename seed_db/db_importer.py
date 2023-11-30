from django.conf import settings
from django.db import transaction

import init_django_orm  # noqa: F401
from seed_db.dto import MoviesDTO
from seed_db.csv_mapper import MovieCSVParser

from movies.models import (
    Genre,
    Certification,
    Director,
    Star,
    Movie,
    MovieGenre,
    MovieDirector,
    MovieStar
)


class MovieDataImporter:
    def __init__(self, movies_dto: MoviesDTO):
        self.movies_dto = movies_dto

    def _get_or_create_genre(self, genre_name: str) -> Genre:
        genre, _ = Genre.objects.get_or_create(name=genre_name)
        return genre

    def _get_or_create_certification(self, certification_name: str) -> Certification:
        certification, _ = Certification.objects.get_or_create(name=certification_name)
        return certification

    def _get_or_create_director(self, director_name: str) -> Director:
        director, _ = Director.objects.get_or_create(name=director_name)
        return director

    def _get_or_create_star(self, star_name: str) -> Star:
        star, _ = Star.objects.get_or_create(name=star_name)
        return star

    @transaction.atomic
    def import_data(self):
        for movie_dto in self.movies_dto.movies:
            certification = self._get_or_create_certification(movie_dto.certification)
            movie = Movie(
                name=movie_dto.name,
                year=movie_dto.year,
                time=movie_dto.time,
                imdb=movie_dto.imdb,
                votes=movie_dto.votes,
                meta_score=movie_dto.meta_score,
                gross=movie_dto.gross,
                certification=certification,
                description=movie_dto.description,
            )
            movie.save()

            for genre_name in movie_dto.genres:
                genre = self._get_or_create_genre(genre_name)
                MovieGenre.objects.create(movie=movie, genre=genre)

            for director_name in movie_dto.directors:
                director = self._get_or_create_director(director_name)
                MovieDirector.objects.create(movie=movie, director=director)

            for star_name in movie_dto.stars:
                star = self._get_or_create_star(star_name)
                MovieStar.objects.create(movie=movie, star=star)


if __name__ == '__main__':
    path_to_movies_file = settings.BASE_DIR / 'seed_db' / 'movies.csv'
    parser = MovieCSVParser(path_to_movies_file)
    movies_dto = parser.read_csv_and_map_to_dto()

    importer = MovieDataImporter(movies_dto)
    importer.import_data()
