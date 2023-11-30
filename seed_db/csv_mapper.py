import ast
import csv
from abc import ABC, abstractmethod
from typing import List, Tuple, Set

from seed_db.dto import MoviesDTO, MovieDTO


class MovieParserInterface(ABC):
    @abstractmethod
    def read_csv_and_map_to_dto(self) -> MoviesDTO:
        pass


class MovieCSVParser(MovieParserInterface):
    def __init__(self, filename: str):
        self.filename = filename

    def _read_csv_file(self) -> List[List[str]]:
        rows = []
        with open(self.filename, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                rows.append(row[1:])
        return rows

    def _map_rows_to_dto(self, movies_rows: List[List[str]]) -> MoviesDTO:
        genres, directors, stars, certifications = self._extract_unique_values(movies_rows)
        movies = [self._create_movie_dto(row) for row in movies_rows]
        return MoviesDTO(genres, certifications, directors, stars, movies)

    def _extract_unique_values(self, movies_rows: List[List[str]]) -> Tuple[Set, Set, Set, Set]:
        genres = set()
        directors = set()
        stars = set()
        certifications = set()

        for row in movies_rows:
            movie_genres = {row_genre.strip() for row_genre in ast.literal_eval(row[7])}
            genres.update(movie_genres)

            movie_directors = {row_director.strip() for row_director in ast.literal_eval(row[9])}
            directors.update(movie_directors)

            movie_stars = {row_star.strip() for row_star in ast.literal_eval(row[10])}
            stars.update(movie_stars)

            certification = row[8].strip()
            movie_certification = certification if certification else 'Not Rated'
            certifications.add(movie_certification)

        return genres, directors, stars, certifications

    def _create_movie_dto(self, row: List[str]) -> MovieDTO:
        name = row[0].strip()
        year = int(row[1])
        time = int(row[2])
        imdb = float(row[3])
        votes = int(row[4])
        meta_score = float(row[5]) if row[5].strip() else None
        gross = float(row[6]) if row[6].strip() else None

        movie_genres = {row_genre.strip() for row_genre in ast.literal_eval(row[7])}
        certification = row[8].strip() or 'Not Rated'
        movie_directors = {row_director.strip() for row_director in ast.literal_eval(row[9])}
        movie_stars = {row_star.strip() for row_star in ast.literal_eval(row[10])}
        description = ' '.join([desc.strip() for desc in ast.literal_eval(row[11])])

        return MovieDTO(
            name=name,
            year=year,
            time=time,
            imdb=imdb,
            votes=votes,
            meta_score=meta_score,
            gross=gross,
            genres=movie_genres,
            certification=certification,
            directors=movie_directors,
            stars=movie_stars,
            description=description
        )

    def read_csv_and_map_to_dto(self) -> MoviesDTO:
        movies_rows = self._read_csv_file()
        movies_dto = self._map_rows_to_dto(movies_rows)
        return movies_dto


def check_duplicates():
    movies_dict = {}
    duplicates = []

    with open('movies.csv', 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            movie_name, movie_year = row[1], row[2]
            if (movie_name, movie_year) in movies_dict:
                duplicates.append(row)
                duplicates.append(movies_dict[(movie_name, movie_year)])
            movies_dict[(movie_name, movie_year)] = row

    unique_duplicates = [list(x) for x in set(tuple(x) for x in duplicates)]
    for dup in unique_duplicates:
        print(dup)


if __name__ == '__main__':
    # parser = MovieCSVParser(MOVIES_FILENAME)
    # movies = parser.read_csv_and_map_to_dto()
    # check_duplicates()
    pass

