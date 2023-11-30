from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import ListView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from movies.models import Movie
from movies.serializers import MovieSerializer


def movie_list_view(request: HttpRequest) -> HttpResponse:
    movies = Movie.objects.all()[:5]
    context = {"movies": movies,}
    return render(request, "movies/movies_list.html", context=context)


class MovieListView(ListView):
    model = Movie
    template_name = "movies/movies_list.html"
    context_object_name = "movies"
    paginate_by = 4

    def get_queryset(self):
        genre_filter = self.request.GET.get("genre")
        queryset = super().get_queryset()
        if genre_filter:
            queryset = queryset.filter(movie_genres__genre__name=genre_filter)
        return queryset


class MovieListAPI(APIView):
    def get(self, request):
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )
