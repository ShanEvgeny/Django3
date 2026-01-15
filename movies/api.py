from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.db.models import Avg, Count, Min, Max
from django.http import HttpResponse
import openpyxl
from openpyxl.drawing.image import Image
from io import BytesIO

from movies.models import Genre,TypeMovie,Director,Movie,RatingMovie
from movies.serializers import GenreSerializer, TypeMovieSerializer, DirectorSerializer, MovieSerializer, RatingMovieSerializer
from movies.permissions import IsModerator, SecondFactorPermission

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
        elif self.action == 'update' or self.action == 'partial_update':
            permission_classes = [(IsModerator & SecondFactorPermission) | (IsAdminUser & SecondFactorPermission)]
        else:
            permission_classes = [IsModerator | IsAdminUser]
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
        elif self.action == 'update' or self.action == 'partial_update':
            permission_classes = [(IsModerator & SecondFactorPermission) | (IsAdminUser & SecondFactorPermission)]
        else:
            permission_classes = [IsModerator | IsAdminUser]
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
        elif self.action == 'update' or self.action == 'partial_update':
            permission_classes = [(IsModerator & SecondFactorPermission) | (IsAdminUser & SecondFactorPermission)]
        else:
            permission_classes = [IsModerator | IsAdminUser]
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
    queryset = Movie.objects.select_related('type_movie')\
                            .prefetch_related('directors','genres')\
                            .annotate(avg_rating = Avg('ratingmovie__rating_value')).all()
    serializer_class = MovieSerializer
    def get_permissions(self):
        if self.action == 'list' or  self.action == 'retrieve' or self.action == 'get_stats':
            permission_classes = [IsAuthenticated]
        elif self.action == 'update' or self.action == 'partial_update':
            permission_classes = [(IsModerator & SecondFactorPermission) | (IsAdminUser & SecondFactorPermission)]
        else:
            permission_classes = [IsModerator | IsAdminUser]
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
    @action(url_path='to-excel', methods = ['GET'], detail=False)
    def export_to_excel(self, request, *args, **kwargs):
        movies = self.get_queryset()
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Movies"
        ws.append(["Id","Рейтинг","Название","Год выхода","Описание", "Тип кино","Режиссеры", "Жанры","Картинка"])
        for m in movies:
            dir_to_export = ', '.join([d.full_name for d in m.directors.all()])
            gnr_to_export = ', '.join([g.title for g in m.genres.all()])
            ws.append([m.id, m.avg_rating, m.title, m.year_of_release, 
                       m.brief_information, 
                       m.type_movie.title, 
                       dir_to_export, gnr_to_export,
                       m.picture.name if m.picture else ""])
        buffer = BytesIO()  
        wb.save(buffer)
        buffer.seek(0)
        response = HttpResponse(buffer.getvalue(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="movies.xlsx"'
        return response
class RatingMoviesViewset(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet):
    queryset = RatingMovie.objects.select_related('movie','user').all()
    serializer_class = RatingMovieSerializer
    def get_permissions(self):
        if self.action == 'update' or self.action == 'partial_update':
            permission_classes = [SecondFactorPermission]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    def get_queryset(self):
        qs = super().get_queryset()
        if (self.request.user.is_staff == False):
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