from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class Certification(models.Model):
    name = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class Director(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class Star(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class Movie(models.Model):
    name = models.CharField(max_length=250)
    year = models.IntegerField()
    time = models.IntegerField()
    imdb = models.FloatField()
    votes = models.IntegerField()
    meta_score = models.FloatField(null=True)
    gross = models.FloatField(null=True)
    certification = models.ForeignKey(Certification, on_delete=models.PROTECT, related_name='movies')
    description = models.TextField()

    def __str__(self):
        return f"{self.name} ({self.year})"

    class Meta:
        ordering = ('name', 'year')


class MovieGenre(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='movie_genres')
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name='genre_movies')

    def __str__(self):
        return f"{self.movie} - {self.genre}"

    class Meta:
        unique_together = ('movie', 'genre')


class MovieDirector(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='movie_directors')
    director = models.ForeignKey(Director, on_delete=models.CASCADE, related_name='director_movies')

    def __str__(self):
        return f"{self.movie} - {self.director}"

    class Meta:
        unique_together = ('movie', 'director')


class MovieStar(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='movie_stars')
    star = models.ForeignKey(Star, on_delete=models.CASCADE, related_name='star_movies')

    def __str__(self):
        return f"{self.movie} - {self.star}"

    class Meta:
        unique_together = ('movie', 'star')
