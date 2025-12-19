from django.contrib import admin
from movies.models import Genre, TypeMovie, Director, Movie, RatingMovie

@admin.register(TypeMovie)
class TypeMovieAdmin(admin.ModelAdmin):
    list_display = ['id','title','description']
@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['id','title','description']
@admin.register(Director)
class DirectorAdmin(admin.ModelAdmin):
    list_display = ['id','full_name','date_of_birth']
@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['id','title','year_of_release','type_movie','brief_information']
    filter_horizontal = ['genres','directors']
@admin.register(RatingMovie)
class RatingMovieAdmin(admin.ModelAdmin):
    list_display = ['id','rating_value','movie']