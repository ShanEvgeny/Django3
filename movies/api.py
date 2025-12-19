from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from movies.models import Genre,TypeMovie,Director,Movie,RatingMovie
from movies.serializers import GenreSerializer, TypeMovieSerializer, DirectorSerializer, MovieSerializer, RatingMovieSerializer

class GenresViewset(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
class DirectorsViewset(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer
class TypeMoviesViewset(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet):
    queryset = TypeMovie.objects.all()
    serializer_class = TypeMovieSerializer
class MoviesViewset(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
class RatingMoviesViewset(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet):
    queryset = RatingMovie.objects.all()
    serializer_class = RatingMovieSerializer