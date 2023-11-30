from rest_framework import serializers

from movies.models import Movie, Genre, Director, Star


class MovieSerializer(serializers.ModelSerializer):
    movie_genres = serializers.PrimaryKeyRelatedField(
        queryset=Genre.objects.all(), many=True
    )
    movie_directors = serializers.PrimaryKeyRelatedField(
        queryset=Director.objects.all(), many=True
    )
    movie_stars = serializers.PrimaryKeyRelatedField(
        queryset=Star.objects.all(), many=True
    )

    class Meta:
        model = Movie
        fields = '__all__'

    def create(self, validated_data):
        genres_data = validated_data.pop("movie_genres")
        directors_data = validated_data.pop("movie_directors")
        stars_data = validated_data.pop("movie_stars")
        movie = Movie.objects.create(**validated_data)
        movie.movie_genres.set(genres_data)
        movie.movie_directors.set(directors_data)
        movie.movie_stars.set(stars_data)
        return movie

    def update(self, instance, validated_data):
        genres_data = validated_data.pop("movie_genres", [])
        directors_data = validated_data.pop("movie_directors", [])
        stars_data = validated_data.pop("movie_stars", [])
        instance = super().update(instance, validated_data)
        instance.movie_genres.set(genres_data)
        instance.movie_directors.set(directors_data)
        instance.movie_stars.set(stars_data)
        return instance
