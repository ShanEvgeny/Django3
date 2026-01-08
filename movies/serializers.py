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
    avg_rating = serializers.FloatField(read_only=True)
    class Meta:
        model = Movie
        fields = '__all__'
class RatingMovieSerializer(serializers.ModelSerializer):
    def create(self, validated_data): 
        if 'request' in self.context:
            validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
    class Meta:
        model = RatingMovie
        fields = '__all__'