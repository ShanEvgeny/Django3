from django.core.management.base import BaseCommand

from faker import Faker

from movies.models import Movie, Director, Genre, TypeMovie, RatingMovie
from django.contrib.auth.models import User
import random
from datetime import datetime
from django.db.utils import IntegrityError

class Command(BaseCommand):
    def handle(self, *args, **options):
        fake = Faker(['ru_RU'])
        genres = list(Genre.objects.all())
        type_movies = TypeMovie.objects.all()
        for _ in range(1000):
            Director.objects.create(
                full_name = fake.name(),
                date_of_birth = fake.date_of_birth(minimum_age=23),
                short_biography = fake.text(max_nb_chars=200)
            )
        directors = list(Director.objects.all())
        for _ in range(1000):
            movie = Movie.objects.create(
                title = fake.sentence(nb_words=random.randint(1,4)),
                year_of_release = fake.random_int(min=1895,max=datetime.now().year),
                type_movie = random.choice(type_movies),
                brief_information = fake.text(max_nb_chars=300)
            )
            movie.directors.set(random.sample(directors,random.randint(1,3)))
            movie.genres.set(random.sample(genres,random.randint(1,5)))
        movies = Movie.objects.all()
        users = User.objects.all()
        for _ in range(1000):
            try:
                RatingMovie.objects.create(
                    rating_value = fake.random_int(min=1,max=10),
                    movie = random.choice(movies),
                    user = random.choice(users)
                ) 
            except IntegrityError: print("Не получилось")


