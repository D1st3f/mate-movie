from django.urls import path

from movies.views import movie_list_view, MovieListView

urlpatterns = [
    # path('', movie_list_view, name="movie_list"),
    path('', MovieListView.as_view(), name='movie_list')
]

app_name = "movies"
