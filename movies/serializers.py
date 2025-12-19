from rest_framework import serializers
from movies.models import Genre, Director, TypeMovie, Movie, RatingMovie

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'
class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = '__all__'
class TypeMovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeMovie
        fields = '__all__'
class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'
class RatingMovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = RatingMovie
        fields = '__all__'