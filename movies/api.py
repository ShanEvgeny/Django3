from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from django.db.models import Avg, Count, Min, Max

from movies.models import Genre,TypeMovie,Director,Movie,RatingMovie
from movies.serializers import GenreSerializer, TypeMovieSerializer, DirectorSerializer, MovieSerializer, RatingMovieSerializer
from movies.permissions import IsModerator

class GenresViewset(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    def get_permissions(self):
        if self.action == 'list' or  self.action == 'retrieve' or self.action == 'get_stats':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsModerator]
        return [permission() for permission in permission_classes]
    class StatsSerializer(serializers.Serializer):
        count = serializers.IntegerField()
        min = serializers.IntegerField()
        max = serializers.IntegerField()
        most_popular_genre = serializers.CharField()
    @action(url_path='stats', methods = ['GET'], detail=False)
    def get_stats(self, request, *args, **kwargs):
        stats_data = Genre.objects.annotate(movie_count = Count('movie_genres'))
        stats = stats_data.aggregate(
            count = Count('*'),
            min = Min('movie_count'),
            max = Max('movie_count'),
        )
        stats['most_popular_genre'] = stats_data.order_by('movie_count').last().title
        serializer = self.StatsSerializer(instance = stats)
        return Response(serializer.data)
class DirectorsViewset(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer
    def get_permissions(self):
        if self.action == 'list' or  self.action == 'retrieve' or self.action == 'get_stats':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsModerator]
        return [permission() for permission in permission_classes]
    class StatsSerializer(serializers.Serializer):
        count_directors = serializers.IntegerField()
        avg_birthday = serializers.FloatField()
        earliest_birthday = serializers.IntegerField()
        latest_birthday = serializers.IntegerField()
        most_productive_director = serializers.CharField()
    @action(url_path='stats', methods = ['GET'], detail=False)
    def get_stats(self, request, *args, **kwargs):
        stats = Director.objects.aggregate(
            count_directors = Count('*'),
            avg_birthday = Avg('date_of_birth__year'),
            earliest_birthday = Min('date_of_birth__year'),
            latest_birthday = Max('date_of_birth__year'),
        )
        stats['most_productive_director'] = Director.objects.annotate(movie_count = Count('movie_directors')).order_by('movie_count').last().full_name
        serializer = self.StatsSerializer(instance = stats)
        return Response(serializer.data)
class TypeMoviesViewset(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet):
    queryset = TypeMovie.objects.all()
    serializer_class = TypeMovieSerializer
    def get_permissions(self):
        if self.action == 'list' or  self.action == 'retrieve' or self.action == 'get_stats':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsModerator]
        return [permission() for permission in permission_classes]
    class StatsSerializer(serializers.Serializer):
        count = serializers.IntegerField()
        min = serializers.IntegerField()
        max = serializers.IntegerField()
        most_popular_type_movie = serializers.CharField()
    @action(url_path='stats', methods = ['GET'], detail=False)
    def get_stats(self, request, *args, **kwargs):
        stats_data = TypeMovie.objects.annotate(movie_count = Count('movie'))
        stats = stats_data.aggregate(
            count = Count('*'),
            min = Min('movie_count'),
            max = Max('movie_count'),
        )
        stats['most_popular_type_movie'] = stats_data.order_by('movie_count').last().title
        serializer = self.StatsSerializer(instance = stats)
        return Response(serializer.data)
class MoviesViewset(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet):
    queryset = Movie.objects.annotate(avg_rating = Avg('ratingmovie__rating_value')).all()
    serializer_class = MovieSerializer
    def get_permissions(self):
        if self.action == 'list' or  self.action == 'retrieve' or self.action == 'get_stats':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsModerator]
        return [permission() for permission in permission_classes]
    class StatsSerializer(serializers.Serializer):
        count_movies = serializers.IntegerField()
        avg_year_of_release = serializers.FloatField()
        oldest_movie = serializers.IntegerField()
        newest_movie = serializers.IntegerField()
        best_movie = serializers.CharField()
    @action(url_path='stats', methods = ['GET'], detail=False)
    def get_stats(self, request, *args, **kwargs):
        stats = Movie.objects.aggregate(
            count_movies = Count('*'),
            avg_year_of_release = Avg('year_of_release'),
            newest_movie = Max('year_of_release'),
            oldest_movie = Min('year_of_release'),
        )
        stats['best_movie'] = self.queryset.order_by('avg_rating').last().title
        serializer = self.StatsSerializer(instance = stats)
        return Response(serializer.data)
class RatingMoviesViewset(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet):
    queryset = RatingMovie.objects.all()
    serializer_class = RatingMovieSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        qs = super().get_queryset()
        if (self.request.user.is_superuser == False):
            qs = qs.filter(user=self.request.user)
        return qs
    class StatsSerializer(serializers.Serializer):
        count_ratings = serializers.IntegerField()
        avg_rating = serializers.FloatField()
        min_rating = serializers.IntegerField()
        max_rating = serializers.IntegerField()

    @action(url_path='stats', methods = ['GET'], detail=False)
    def get_stats(self, request, *args, **kwargs):
        stats = self.queryset.aggregate(
            count_ratings = Count('*'),
            avg_rating = Avg('rating_value'),
            min_rating = Min('rating_value'),
            max_rating = Max('rating_value'),
        )
        serializer = self.StatsSerializer(instance = stats)
        return Response(serializer.data)