from rest_framework import serializers
from django.db.models import Avg
from movies.models import Movie


class MovieModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = '__all__'

    # Validar POST
    def validate_release_date(self, value):

        if value.year < 1900:
            raise serializers.ValidationError('A data de lançamento não pode ser inferior que 1990')
        return value

    def validate_resume(self, value):

        if len(value) > 200:
            raise serializers.ValidationError('O resumo deve ter menos que 200 caracteres')
        return value


class MovieListDetailSerializer(serializers.ModelSerializer):
    rate = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Movie
        fields = '__all__'
    
    # Soma média das estrelas em Reviews de cada filme
    def get_rate(self, obj):
        rate = obj.reviews.aggregate(Avg('stars'))['stars__avg']

        if rate:
            return round(rate, 1)

        return None


class MovieStatsSerializer(serializers.Serializer):
    total_movies = serializers.IntegerField()
    movies_by_genre = serializers.ListField()
    total_reviews = serializers.IntegerField()
    average_stars = serializers.FloatField()