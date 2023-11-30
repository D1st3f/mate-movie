from typing import Optional
from dataclasses import dataclass


@dataclass
class MovieDTO:
    name: str
    year: int
    time: int
    imdb: float
    votes: int
    meta_score: Optional[float]
    gross: Optional[float]
    genres: set[str]
    certification: str
    directors: set[str]
    stars: set[str]
    description: str


@dataclass
class MoviesDTO:
    genres: set
    certifications: set
    directors: set
    stars: set
    movies: list[MovieDTO]
